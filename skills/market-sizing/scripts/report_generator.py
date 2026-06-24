"""
Excel-first market sizing report generator.

The workbook is the calculation surface. Markdown is an explanatory memo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
except ImportError as exc:  # pragma: no cover - import guard
    raise ImportError("Please install openpyxl: pip install openpyxl") from exc


RATE_KEYWORDS = (
    "rate",
    "ratio",
    "share",
    "pct",
    "penetration",
    "pene",
    "adopt",
    "率",
    "占比",
    "份额",
    "渗透",
    "采用",
)


@dataclass
class MarketSizingData:
    market_name: str
    geography: str
    base_year: int
    forecast_years: int
    tam: float
    sam: float
    som: float
    unit: str
    cagr: float
    core_insight: Optional[str] = None
    market_definition: Dict[str, Dict[str, str]] = field(default_factory=dict)
    source_cards: List[Dict[str, Any]] = field(default_factory=list)
    assumptions: List[Dict[str, Any]] = field(default_factory=list)
    calculation_lines: List[Dict[str, Any]] = field(default_factory=list)
    market_segments: List[Dict[str, Any]] = field(default_factory=list)
    side_checks: List[Dict[str, Any]] = field(default_factory=list)
    risks: List[Dict[str, Any]] = field(default_factory=list)
    growth_drivers: List[str] = field(default_factory=list)
    competitors: List[Dict[str, Any]] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        errors: List[str] = []

        if self.forecast_years < 1:
            errors.append("forecast_years must be at least 1.")

        if not self.assumptions:
            errors.append("assumptions is required; Excel formulas need editable inputs.")
            return errors

        keys = []
        for i, item in enumerate(self.assumptions, start=1):
            key = str(item.get("key", "")).strip()
            name = str(item.get("name", key)).strip()
            if not key:
                errors.append(f"assumption #{i} is missing key.")
                continue
            if key in keys:
                errors.append(f"duplicate assumption key: {key}")
            keys.append(key)
            if item.get("numeric_value") is None:
                errors.append(f"assumption '{name}' is missing numeric_value.")
            if _is_rate_like(key, name) and not str(item.get("logic", "")).strip():
                errors.append(
                    f"assumption '{name}' ({key}) is a rate/share/ratio and must include logic."
                )

        key_set = set(keys)
        for required in ("sam_ratio", "som_share"):
            if required not in key_set:
                errors.append(f"missing required assumption key: {required}")

        source_ids = {
            str(card.get("source_id")).strip()
            for card in self.source_cards
            if str(card.get("source_id", "")).strip()
        }
        for item in self.assumptions:
            source_ref = str(item.get("source_ref", "")).strip()
            if source_ref and source_ids and source_ref not in source_ids:
                errors.append(
                    f"assumption '{item.get('key')}' refers to unknown source_ref '{source_ref}'."
                )

        for i, segment in enumerate(self.market_segments, start=1):
            name = str(segment.get("name", "")).strip()
            if not name:
                errors.append(f"market_segment #{i} is missing name.")
            if segment.get("base_value") is None:
                errors.append(f"market_segment '{name or i}' is missing base_value.")
            logic = str(segment.get("logic", "")).strip()
            source_ref = str(segment.get("source_ref", "")).strip()
            if source_ref and source_ids and source_ref not in source_ids:
                errors.append(
                    f"market_segment '{name or i}' refers to unknown source_ref '{source_ref}'."
                )
            if not source_ref and not logic:
                errors.append(
                    f"market_segment '{name or i}' must include source_ref or logic."
                )

        for line in self.calculation_lines:
            formula = str(line.get("excel_formula", ""))
            for token in re.findall(r"\{([A-Za-z0-9_\-.]+)\}", formula):
                if token not in key_set:
                    errors.append(
                        f"calculation line '{line.get('label', '')}' references unknown key '{token}'."
                    )

        if not self.calculation_lines and not self._has_auto_formula_pattern(key_set):
            errors.append(
                "cannot build TAM formula from assumptions; provide calculation_lines or a supported key pattern."
            )

        return errors

    @staticmethod
    def _has_auto_formula_pattern(keys: set[str]) -> bool:
        if {"base_pop", "core_pop_pct", "pene_rate", "freq", "price"}.issubset(keys):
            return True
        if {"existing_market", "substitution_rate"}.issubset(keys):
            return True
        if {"end_market", "value_share"}.issubset(keys):
            return True
        if {"target_count", "prob_cost", "wtp_ratio"}.issubset(keys):
            return True

        prefixes = set()
        for key in keys:
            if "_" in key:
                prefixes.add(key.rsplit("_", 1)[0])
        for prefix in prefixes:
            has_count = f"{prefix}_count" in keys or f"{prefix}_vol" in keys
            has_rate = (
                f"{prefix}_adopt" in keys
                or f"{prefix}_rate" in keys
                or f"{prefix}_penetration" in keys
            )
            has_price = f"{prefix}_price" in keys or f"{prefix}_arpu" in keys
            if has_count and has_rate and has_price:
                return True
        return False


class ReportGenerator:
    def generate(
        self,
        data: MarketSizingData,
        output_dir: str | Path,
        formats: Optional[Iterable[str]] = None,
    ) -> Dict[str, Path]:
        formats = list(formats or ["xlsx", "md"])
        unsupported = sorted(set(formats) - {"xlsx", "md"})
        if unsupported:
            raise ValueError(f"Unsupported output formats: {', '.join(unsupported)}")

        errors = data.validate()
        if errors:
            raise ValueError("Market sizing data failed validation:\n- " + "\n- ".join(errors))

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        base_name = f"market_sizing_{_safe_filename(data.market_name)}_{date.today():%Y%m%d}"

        results: Dict[str, Path] = {}
        if "xlsx" in formats:
            path = output_path / f"{base_name}.xlsx"
            self.generate_excel(data, path)
            results["xlsx"] = path
        if "md" in formats:
            path = output_path / f"{base_name}.md"
            self.generate_markdown(data, path, results.get("xlsx"))
            results["md"] = path
        return results

    def generate_markdown(
        self,
        data: MarketSizingData,
        output_path: str | Path,
        workbook_path: Optional[Path] = None,
    ) -> str:
        lines: List[str] = []
        lines.append(f"# {data.market_name} 市场规模测算")
        lines.append("")
        lines.append(f"> 地域：{data.geography}")
        lines.append(f"> 基准年：{data.base_year}")
        lines.append(f"> 单位：{data.unit}")
        if workbook_path:
            lines.append(f"> Excel 模型：{workbook_path.name}")
        lines.append("")

        lines.append("## 1. 核心结论")
        lines.append("")
        lines.append("核心结果在 Excel 的 `核心结论` 工作表第一页展示；`TAM_SAM_SOM` 保留公式明细。")
        lines.append("")
        lines.append("| 年份 | TAM | SAM | SOM |")
        lines.append("|------|-----|-----|-----|")
        for year, tam, sam, som in _annual_values(data):
            lines.append(
                f"| {year}E | {tam:g} {data.unit} | {sam:g} {data.unit} | {som:g} {data.unit} |"
            )
        lines.append("")
        lines.append("TAM/SAM/SOM 必须按年度展示，不能只给预测期合计。")
        if data.core_insight:
            lines.append("")
            lines.append(data.core_insight)
        lines.append("")

        if data.market_segments:
            lines.append("### TAM 构成")
            lines.append("")
            years = [f"{year}E" for year, *_ in _annual_values(data)]
            lines.append("| 市场组成 | " + " | ".join(years) + " |")
            lines.append("|---" + "|---" * len(years) + "|")
            for name, values in _segment_values(data):
                formatted = [f"{value:g} {data.unit}" for value in values]
                lines.append("| " + name + " | " + " | ".join(formatted) + " |")
            lines.append("")

        if data.market_definition:
            lines.append("## 2. 市场定义")
            lines.append("")
            lines.append("| 维度 | 包含 | 排除 |")
            lines.append("|------|------|------|")
            for dim, scope in data.market_definition.items():
                lines.append(
                    f"| {dim} | {scope.get('in', scope.get('包含', ''))} | {scope.get('out', scope.get('排除', ''))} |"
                )
            lines.append("")

        lines.append("## 3. 公式链")
        lines.append("")
        lines.append("核心公式保存在 Excel 的 `Calculation_Model` 与 `TAM_SAM_SOM` 工作表中，年度口径在 `核心结论` 首页同步引用。")
        lines.append("")
        lines.append("| Key | 假设 | 数值 | 单位 | Source | 逻辑 |")
        lines.append("|-----|------|------|------|--------|------|")
        for item in data.assumptions:
            lines.append(
                "| {key} | {name} | {value} | {unit} | {source} | {logic} |".format(
                    key=item.get("key", ""),
                    name=item.get("name", ""),
                    value=item.get("numeric_value", ""),
                    unit=item.get("unit", ""),
                    source=item.get("source_ref", item.get("source", "")),
                    logic=str(item.get("logic", "")).replace("\n", " "),
                )
            )
        lines.append("")

        if data.source_cards:
            lines.append("## 4. Source Cards")
            lines.append("")
            lines.append("| ID | Provider | Metric | Period | Unit | Used In |")
            lines.append("|----|----------|--------|--------|------|---------|")
            for card in data.source_cards:
                lines.append(
                    "| {id} | {provider} | {metric} | {period} | {unit} | {used} |".format(
                        id=card.get("source_id", ""),
                        provider=card.get("provider", ""),
                        metric=card.get("metric", card.get("dataset_or_title", "")),
                        period=card.get("period", ""),
                        unit=card.get("unit", ""),
                        used=card.get("used_in", ""),
                    )
                )
            lines.append("")

        if data.side_checks:
            lines.append("## 5. Side Check")
            lines.append("")
            lines.append("| 方法 | 结果 | 解释 |")
            lines.append("|------|------|------|")
            for item in data.side_checks:
                lines.append(
                    f"| {item.get('method', '')} | {item.get('result', '')} | {item.get('interpretation', '')} |"
                )
            lines.append("")

        lines.append("## 6. 局限与下一步")
        lines.append("")
        if data.risks:
            for item in data.risks:
                lines.append(f"- {item.get('type', '风险')}: {item.get('detail', '')}")
        else:
            lines.append("- 优先补充对结果最敏感的比例、价格或可服务范围数据。")
        lines.append("")

        content = "\n".join(lines)
        Path(output_path).write_text(content, encoding="utf-8")
        return content

    def generate_excel(self, data: MarketSizingData, output_path: str | Path) -> str:
        wb = Workbook()
        wb.remove(wb.active)

        styles = _Styles()
        ws_overview = wb.create_sheet("核心结论")

        ws_def = wb.create_sheet("Market_Definition")
        self._write_market_definition(ws_def, data, styles)

        ws_src = wb.create_sheet("Source_Cards")
        self._write_source_cards(ws_src, data, styles)

        ws_assump = wb.create_sheet("Assumptions")
        key_map = self._write_assumptions(ws_assump, data, styles)

        ws_calc = wb.create_sheet("Calculation_Model")
        tam_cell = self._write_calculation_model(ws_calc, data, key_map, styles)

        ws_out = wb.create_sheet("TAM_SAM_SOM")
        annual_info = self._write_outputs(ws_out, data, key_map, tam_cell, styles)
        self._write_overview(ws_overview, data, annual_info, styles)

        ws_checks = wb.create_sheet("Checks")
        self._write_checks(ws_checks, data, key_map, styles, annual_info)

        for sheet in wb.worksheets:
            sheet.freeze_panes = "A2"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(output_path)
        return str(output_path)

    def _write_overview(
        self,
        ws,
        data: MarketSizingData,
        annual_info: Dict[str, Any],
        styles: "_Styles",
    ) -> None:
        ws["A1"] = f"{data.market_name} | 市场规模核心结论"
        ws["A1"].font = Font(bold=True, size=16, color="1F4E79")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=7)

        meta_rows = [
            ("地域", data.geography),
            ("预测期", f"{data.base_year}E-{data.base_year + data.forecast_years - 1}E"),
            ("单位", data.unit),
            ("口径", "年度市场规模，不是预测期合计。"),
        ]
        for row_idx, (label, value) in enumerate(meta_rows, start=3):
            ws.cell(row_idx, 1, label)
            ws.cell(row_idx, 2, value)
            _style_row(ws, row_idx, 2, styles)

        years = [data.base_year + offset for offset in range(data.forecast_years)]
        start_row = 8
        _write_header(ws, start_row, ["指标"] + [f"{year}E" for year in years], styles)
        metric_rows = [
            ("TAM", annual_info["tam_col"]),
            ("SAM", annual_info["sam_col"]),
            ("SOM", annual_info["som_col"]),
        ]
        for row_offset, (metric, source_col) in enumerate(metric_rows, start=1):
            row = start_row + row_offset
            ws.cell(row, 1, metric)
            for offset in range(data.forecast_years):
                source_row = annual_info["first_annual_row"] + offset
                source_cell = f"{get_column_letter(source_col)}{source_row}"
                cell = ws.cell(row, 2 + offset, f"={_sheet_cell(annual_info['sheet'], source_cell)}")
                cell.fill = styles.formula_fill
                cell.number_format = "#,##0.00"
            _style_row(ws, row, 1 + data.forecast_years, styles)

        note_row = start_row + 5
        ws.cell(note_row, 1, "一句话判断")
        ws.cell(note_row, 1).font = styles.subtitle
        ws.cell(note_row + 1, 1, data.core_insight or "请在这里写清市场量级、最大组成部分和最影响结论的变量。")
        ws.merge_cells(
            start_row=note_row + 1,
            start_column=1,
            end_row=note_row + 2,
            end_column=1 + data.forecast_years,
        )
        _style_row(ws, note_row + 1, 1 + data.forecast_years, styles)

        segment_start = note_row + 5
        _write_header(
            ws,
            segment_start,
            ["TAM 市场组成"] + [f"{year}E" for year in years] + ["末年占比"],
            styles,
        )
        segment_rows = self._write_segment_rows(ws, data, segment_start + 1, annual_info, styles)

        tip_row = segment_rows["last_row"] + 3
        ws.cell(tip_row, 1, "阅读提示")
        ws.cell(tip_row, 1).font = styles.subtitle
        tips = [
            "黄色单元格是输入，绿色单元格是公式。",
            "比例、渗透率、市占率等假设必须回到 Assumptions 的 logic 字段。",
            "若市场组成合计与 TAM 不一致，Checks 会提示修正口径。",
        ]
        for offset, tip in enumerate(tips, start=1):
            ws.cell(tip_row + offset, 1, tip)
            _style_row(ws, tip_row + offset, 1 + data.forecast_years, styles)

        _set_widths(ws, [28] + [16] * data.forecast_years + [14])

    def _write_segment_rows(
        self,
        ws,
        data: MarketSizingData,
        start_row: int,
        annual_info: Dict[str, Any],
        styles: "_Styles",
    ) -> Dict[str, int]:
        rows = []
        if data.market_segments:
            rows = data.market_segments
        else:
            rows = [{"name": "总 TAM", "base_value": None, "growth_rate": None}]

        value_cols = list(range(2, 2 + data.forecast_years))
        last_value_col = value_cols[-1]
        first_row = start_row
        for row_offset, segment in enumerate(rows):
            row = start_row + row_offset
            ws.cell(row, 1, segment.get("name", f"细分市场 {row_offset + 1}"))
            if data.market_segments:
                growth_rate = segment.get("growth_rate", data.cagr)
                ws.cell(row, value_cols[0], segment.get("base_value"))
                ws.cell(row, value_cols[0]).fill = styles.input_fill
                for col in value_cols[1:]:
                    prev = f"{get_column_letter(col - 1)}{row}"
                    ws.cell(row, col, f"={prev}*(1+{growth_rate})")
                    ws.cell(row, col).fill = styles.formula_fill
            else:
                for offset, col in enumerate(value_cols):
                    source_row = annual_info["first_annual_row"] + offset
                    source_cell = f"{get_column_letter(annual_info['tam_col'])}{source_row}"
                    ws.cell(row, col, f"={_sheet_cell(annual_info['sheet'], source_cell)}")
                    ws.cell(row, col).fill = styles.formula_fill
            for col in value_cols:
                ws.cell(row, col).number_format = "#,##0.00"
            _style_row(ws, row, 2 + data.forecast_years, styles)

        total_row = start_row + len(rows)
        ws.cell(total_row, 1, "合计")
        ws.cell(total_row, 1).font = Font(bold=True)
        for col in value_cols:
            col_letter = get_column_letter(col)
            ws.cell(total_row, col, f"=SUM({col_letter}{first_row}:{col_letter}{total_row - 1})")
            ws.cell(total_row, col).fill = styles.formula_fill
            ws.cell(total_row, col).number_format = "#,##0.00"
        _style_row(ws, total_row, 2 + data.forecast_years, styles)

        for row in range(first_row, total_row):
            ws.cell(row, last_value_col + 1, f"={get_column_letter(last_value_col)}{row}/{get_column_letter(last_value_col)}{total_row}")
            ws.cell(row, last_value_col + 1).fill = styles.formula_fill
            ws.cell(row, last_value_col + 1).number_format = "0.0%"

        ws.cell(total_row, last_value_col + 1, "100.0%")
        _style_row(ws, total_row, last_value_col + 1, styles)
        return {"first_row": first_row, "last_row": total_row, "total_row": total_row}

    def _write_market_definition(self, ws, data: MarketSizingData, styles: "_Styles") -> None:
        ws["A1"] = "Market Definition"
        ws["A1"].font = styles.title
        rows = [
            ("Market", data.market_name),
            ("Geography", data.geography),
            ("Base Year", data.base_year),
            ("Forecast Years", data.forecast_years),
            ("Unit", data.unit),
            ("Core Insight", data.core_insight or ""),
        ]
        for i, (label, value) in enumerate(rows, start=3):
            ws.cell(i, 1, label)
            ws.cell(i, 2, value)
            _style_row(ws, i, 2, styles)

        start = 11
        _write_header(ws, start, ["Dimension", "In Scope", "Out of Scope"], styles)
        for offset, (dim, scope) in enumerate(data.market_definition.items(), start=1):
            row = start + offset
            ws.cell(row, 1, dim)
            ws.cell(row, 2, scope.get("in", scope.get("包含", "")))
            ws.cell(row, 3, scope.get("out", scope.get("排除", "")))
            _style_row(ws, row, 3, styles)
        _set_widths(ws, [24, 48, 48])

    def _write_source_cards(self, ws, data: MarketSizingData, styles: "_Styles") -> None:
        ws["A1"] = "Source Cards"
        ws["A1"].font = styles.title
        headers = [
            "source_id",
            "provider",
            "dataset_or_title",
            "metric",
            "geography",
            "period",
            "unit",
            "value_or_path",
            "url_or_endpoint",
            "accessed_at",
            "last_updated_or_vintage",
            "transform_note",
            "used_in",
        ]
        _write_header(ws, 3, headers, styles)
        for row_idx, card in enumerate(data.source_cards, start=4):
            for col_idx, key in enumerate(headers, start=1):
                ws.cell(row_idx, col_idx, card.get(key, ""))
            _style_row(ws, row_idx, len(headers), styles)
        _set_widths(ws, [14, 20, 28, 24, 16, 14, 14, 28, 42, 14, 20, 36, 18])

    def _write_assumptions(self, ws, data: MarketSizingData, styles: "_Styles") -> Dict[str, str]:
        ws["A1"] = "Assumptions"
        ws["A1"].font = styles.title
        headers = ["key", "name", "numeric_value", "unit", "source_ref", "logic", "used_in"]
        _write_header(ws, 3, headers, styles)
        key_map: Dict[str, str] = {}
        for row_idx, item in enumerate(data.assumptions, start=4):
            values = [
                item.get("key", ""),
                item.get("name", ""),
                item.get("numeric_value", ""),
                item.get("unit", ""),
                item.get("source_ref", item.get("source", "")),
                item.get("logic", ""),
                item.get("used_in", ""),
            ]
            for col_idx, value in enumerate(values, start=1):
                ws.cell(row_idx, col_idx, value)
            ws.cell(row_idx, 3).fill = styles.input_fill
            ws.cell(row_idx, 3).number_format = "0.0000"
            _style_row(ws, row_idx, len(headers), styles)
            key = str(item.get("key", "")).strip()
            if key:
                key_map[key] = f"Assumptions!$C${row_idx}"
        _set_widths(ws, [22, 28, 16, 12, 16, 72, 18])
        return key_map

    def _write_calculation_model(
        self,
        ws,
        data: MarketSizingData,
        key_map: Dict[str, str],
        styles: "_Styles",
    ) -> str:
        ws["A1"] = "Calculation Model"
        ws["A1"].font = styles.title
        _write_header(ws, 3, ["Step", "Logic", f"Formula / Value ({data.unit})", "Unit", "Note"], styles)

        if data.calculation_lines:
            tam_row = self._write_custom_calculation_lines(ws, data, key_map, styles)
            return f"Calculation_Model!$C${tam_row}"

        keys = set(key_map)
        if {"base_pop", "core_pop_pct", "pene_rate", "freq", "price"}.issubset(keys):
            tam_row = self._write_population_model(ws, data, key_map, styles)
        elif {"existing_market", "substitution_rate"}.issubset(keys):
            tam_row = self._write_substitution_model(ws, data, key_map, styles)
        elif {"end_market", "value_share"}.issubset(keys):
            tam_row = self._write_value_chain_model(ws, data, key_map, styles)
        elif {"target_count", "prob_cost", "wtp_ratio"}.issubset(keys):
            tam_row = self._write_value_based_model(ws, data, key_map, styles)
        else:
            tam_row = self._write_institution_model(ws, data, key_map, styles)

        _set_widths(ws, [30, 44, 24, 14, 40])
        return f"Calculation_Model!$C${tam_row}"

    def _write_custom_calculation_lines(
        self,
        ws,
        data: MarketSizingData,
        key_map: Dict[str, str],
        styles: "_Styles",
    ) -> int:
        tam_row = 4
        for row_idx, line in enumerate(data.calculation_lines, start=4):
            formula = _replace_formula_tokens(str(line.get("excel_formula", "")), key_map)
            if formula and not formula.startswith("="):
                formula = "=" + formula
            ws.cell(row_idx, 1, line.get("label", f"Step {row_idx - 3}"))
            ws.cell(row_idx, 2, line.get("logic", ""))
            ws.cell(row_idx, 3, formula or line.get("value", ""))
            ws.cell(row_idx, 4, line.get("unit", data.unit))
            ws.cell(row_idx, 5, line.get("note", ""))
            if formula:
                ws.cell(row_idx, 3).fill = styles.formula_fill
            _style_row(ws, row_idx, 5, styles)
            if str(line.get("output_key", "")).lower() == "tam":
                tam_row = row_idx
            else:
                tam_row = row_idx
        return tam_row

    def _write_population_model(self, ws, data, key_map, styles) -> int:
        rows = [
            ("Base population", "亿人 -> 人", f"={key_map['base_pop']}*100000000", "人", "base_pop in 100m people"),
            ("Core population", "Base x core_pop_pct", f"=C4*{key_map['core_pop_pct']}", "人", ""),
            ("Paying/adopting users", "Core x pene_rate", f"=C5*{key_map['pene_rate']}", "人", ""),
            ("Annual transactions", "Users x freq", f"=C6*{key_map['freq']}", "次", ""),
            (
                "TAM",
                "Transactions x price, converted to 亿元 when price is RMB",
                f"=C7*{key_map['price']}/100000000",
                data.unit,
                "Adjust unit conversion if unit is not 亿元.",
            ),
        ]
        return _write_formula_rows(ws, rows, styles)

    def _write_substitution_model(self, ws, data, key_map, styles) -> int:
        premium = key_map.get("price_premium", "1")
        rows = [
            ("Existing market", "Starting market", f"={key_map['existing_market']}", data.unit, ""),
            ("Substitutable market", "Existing market x substitution_rate", f"=C4*{key_map['substitution_rate']}", data.unit, ""),
            ("TAM", "Apply price/value premium", f"=C5*{premium}", data.unit, ""),
        ]
        return _write_formula_rows(ws, rows, styles)

    def _write_value_chain_model(self, ws, data, key_map, styles) -> int:
        rows = [
            ("End market", "Terminal market size", f"={key_map['end_market']}", data.unit, ""),
            ("TAM", "End market x value_share", f"=C4*{key_map['value_share']}", data.unit, ""),
        ]
        return _write_formula_rows(ws, rows, styles)

    def _write_value_based_model(self, ws, data, key_map, styles) -> int:
        freq = key_map.get("prob_freq", "1")
        rows = [
            ("Target count", "Objects with the problem", f"={key_map['target_count']}", "个", ""),
            ("Annual problem events", "Target count x problem frequency", f"=C4*{freq}", "次", ""),
            ("Gross problem value", "Events x problem cost", f"=C5*{key_map['prob_cost']}", data.unit, ""),
            ("TAM", "Gross value x willingness to pay", f"=C6*{key_map['wtp_ratio']}", data.unit, ""),
        ]
        return _write_formula_rows(ws, rows, styles)

    def _write_institution_model(self, ws, data, key_map, styles) -> int:
        prefixes = []
        keys = set(key_map)
        for key in keys:
            if "_" in key:
                prefix = key.rsplit("_", 1)[0]
                has_count = f"{prefix}_count" in keys or f"{prefix}_vol" in keys
                has_rate = (
                    f"{prefix}_adopt" in keys
                    or f"{prefix}_rate" in keys
                    or f"{prefix}_penetration" in keys
                )
                has_price = f"{prefix}_price" in keys or f"{prefix}_arpu" in keys
                if has_count and has_rate and has_price:
                    prefixes.append(prefix)
        prefixes = sorted(set(prefixes))
        if not prefixes:
            raise ValueError("No supported institution-based key pattern found.")

        row = 4
        subtotal_cells = []
        for prefix in prefixes:
            count_key = f"{prefix}_count" if f"{prefix}_count" in key_map else f"{prefix}_vol"
            rate_key = next(
                key
                for key in (f"{prefix}_adopt", f"{prefix}_rate", f"{prefix}_penetration")
                if key in key_map
            )
            price_key = f"{prefix}_price" if f"{prefix}_price" in key_map else f"{prefix}_arpu"
            ws.cell(row, 1, f"{prefix} subtotal")
            ws.cell(row, 2, f"{count_key} x {rate_key} x {price_key}")
            ws.cell(row, 3, f"={key_map[count_key]}*{key_map[rate_key]}*{key_map[price_key]}")
            ws.cell(row, 4, data.unit)
            ws.cell(row, 5, "Institution/customer segment formula")
            ws.cell(row, 3).fill = styles.formula_fill
            _style_row(ws, row, 5, styles)
            subtotal_cells.append(f"C{row}")
            row += 1

        ws.cell(row, 1, "TAM")
        ws.cell(row, 2, "Sum of segment subtotals")
        ws.cell(row, 3, f"=SUM({','.join(subtotal_cells)})")
        ws.cell(row, 4, data.unit)
        ws.cell(row, 5, "")
        ws.cell(row, 3).fill = styles.formula_fill
        _style_row(ws, row, 5, styles)
        return row

    def _write_outputs(self, ws, data, key_map, tam_cell, styles) -> Dict[str, Any]:
        ws["A1"] = "TAM / SAM / SOM"
        ws["A1"].font = styles.title
        _write_header(ws, 3, ["Metric", f"Value ({data.unit})", "Unit", "Formula Logic"], styles)

        segment_total_row = None
        segment_header_row = 13 + data.forecast_years
        if data.market_segments:
            segment_total_row = self._write_output_segment_table(ws, data, segment_header_row, styles)

        rows = [
            (
                "TAM",
                f"=B{segment_total_row}" if segment_total_row else f"={tam_cell}",
                data.unit,
                "Sum of market segments" if segment_total_row else f"Linked from {tam_cell}",
            ),
            ("SAM", f"=B4*{key_map['sam_ratio']}", data.unit, "TAM x sam_ratio"),
            ("SOM", f"=B5*{key_map['som_share']}", data.unit, "SAM x som_share"),
        ]
        for idx, row in enumerate(rows, start=4):
            for col, value in enumerate(row, start=1):
                ws.cell(idx, col, value)
            ws.cell(idx, 2).fill = styles.formula_fill
            ws.cell(idx, 2).number_format = "#,##0.00"
            _style_row(ws, idx, 4, styles)

        _write_header(ws, 9, ["Year", f"TAM ({data.unit})", f"SAM ({data.unit})", f"SOM ({data.unit})"], styles)
        cagr_ref = key_map.get("cagr", str(data.cagr))
        first_annual_row = 10
        for offset in range(data.forecast_years):
            row = 10 + offset
            ws.cell(row, 1, data.base_year + offset)
            if segment_total_row:
                segment_year_col = get_column_letter(2 + offset)
                ws.cell(row, 2, f"={segment_year_col}{segment_total_row}")
            elif offset == 0:
                ws.cell(row, 2, "=B4")
            else:
                ws.cell(row, 2, f"=B{row-1}*(1+{cagr_ref})")
            ws.cell(row, 3, f"=B{row}*{key_map['sam_ratio']}")
            ws.cell(row, 4, f"=C{row}*{key_map['som_share']}")
            for col in range(2, 5):
                ws.cell(row, col).fill = styles.formula_fill
                ws.cell(row, col).number_format = "#,##0.00"
            _style_row(ws, row, 4, styles)

        if data.side_checks:
            start = (segment_total_row + 3) if segment_total_row else (13 + data.forecast_years)
            _write_header(ws, start, ["Side Check", "Result", "Interpretation"], styles)
            for row_offset, item in enumerate(data.side_checks, start=1):
                row = start + row_offset
                ws.cell(row, 1, item.get("method", ""))
                ws.cell(row, 2, item.get("result", ""))
                ws.cell(row, 3, item.get("interpretation", ""))
                _style_row(ws, row, 3, styles)

        _set_widths(ws, [18, 20, 12, 42] + [16] * max(data.forecast_years - 3, 0))
        return {
            "sheet": ws.title,
            "first_annual_row": first_annual_row,
            "last_annual_row": first_annual_row + data.forecast_years - 1,
            "year_col": 1,
            "tam_col": 2,
            "sam_col": 3,
            "som_col": 4,
        }

    def _write_output_segment_table(self, ws, data, start_row: int, styles: "_Styles") -> int:
        years = [f"{data.base_year + offset}E" for offset in range(data.forecast_years)]
        _write_header(ws, start_row, ["TAM 市场组成"] + years, styles)

        value_cols = list(range(2, 2 + data.forecast_years))
        first_row = start_row + 1
        for row_offset, segment in enumerate(data.market_segments):
            row = first_row + row_offset
            ws.cell(row, 1, segment.get("name", f"细分市场 {row_offset + 1}"))
            growth_rate = segment.get("growth_rate", data.cagr)
            ws.cell(row, value_cols[0], segment.get("base_value"))
            ws.cell(row, value_cols[0]).fill = styles.input_fill
            for col in value_cols[1:]:
                prev = f"{get_column_letter(col - 1)}{row}"
                ws.cell(row, col, f"={prev}*(1+{growth_rate})")
                ws.cell(row, col).fill = styles.formula_fill
            for col in value_cols:
                ws.cell(row, col).number_format = "#,##0.00"
            _style_row(ws, row, 1 + data.forecast_years, styles)

        total_row = first_row + len(data.market_segments)
        ws.cell(total_row, 1, "合计")
        ws.cell(total_row, 1).font = Font(bold=True)
        for col in value_cols:
            col_letter = get_column_letter(col)
            ws.cell(total_row, col, f"=SUM({col_letter}{first_row}:{col_letter}{total_row - 1})")
            ws.cell(total_row, col).fill = styles.formula_fill
            ws.cell(total_row, col).number_format = "#,##0.00"
        _style_row(ws, total_row, 1 + data.forecast_years, styles)
        return total_row

    def _write_checks(self, ws, data, key_map, styles, annual_info: Dict[str, Any]) -> None:
        ws["A1"] = "Quality Checks"
        ws["A1"].font = styles.title
        _write_header(ws, 3, ["Check", "Status", "Detail"], styles)

        annual_first = annual_info["first_annual_row"]
        annual_last = annual_info["last_annual_row"]
        tam_col = get_column_letter(annual_info["tam_col"])
        sam_col = get_column_letter(annual_info["sam_col"])
        som_col = get_column_letter(annual_info["som_col"])
        last_overview_col = get_column_letter(1 + data.forecast_years)
        overview_total_row = 18 + 1 + len(data.market_segments or [{"name": "总 TAM"}])
        checks = [
            ("TAM >= SAM", '=IF(TAM_SAM_SOM!B4>=TAM_SAM_SOM!B5,"OK","CHECK")', "Layering order"),
            ("SAM >= SOM", '=IF(TAM_SAM_SOM!B5>=TAM_SAM_SOM!B6,"OK","CHECK")', "Layering order"),
            (
                "Annual TAM >= SAM >= SOM",
                (
                    f'=IF(AND(SUMPRODUCT(--(TAM_SAM_SOM!{tam_col}{annual_first}:{tam_col}{annual_last}>='
                    f'TAM_SAM_SOM!{sam_col}{annual_first}:{sam_col}{annual_last}))={data.forecast_years},'
                    f'SUMPRODUCT(--(TAM_SAM_SOM!{sam_col}{annual_first}:{sam_col}{annual_last}>='
                    f'TAM_SAM_SOM!{som_col}{annual_first}:{som_col}{annual_last}))={data.forecast_years}),"OK","CHECK")'
                ),
                "Annual rows must preserve TAM/SAM/SOM hierarchy",
            ),
            (
                "Overview segment total matches TAM",
                (
                    f'=IF(ABS(\'核心结论\'!{last_overview_col}{overview_total_row}'
                    f'-TAM_SAM_SOM!{tam_col}{annual_last})<=MAX(0.01,'
                    f'TAM_SAM_SOM!{tam_col}{annual_last}*0.01),"OK","CHECK")'
                ),
                "Last-year TAM composition should reconcile with total TAM",
            ),
            ("SAM formula uses sam_ratio", "OK" if "sam_ratio" in key_map else "CHECK", "Required assumption"),
            ("SOM formula uses som_share", "OK" if "som_share" in key_map else "CHECK", "Required assumption"),
        ]
        row = 4
        for check, status, detail in checks:
            ws.cell(row, 1, check)
            ws.cell(row, 2, status)
            ws.cell(row, 3, detail)
            _style_row(ws, row, 3, styles)
            row += 1

        source_ids = {
            str(card.get("source_id")).strip()
            for card in data.source_cards
            if str(card.get("source_id", "")).strip()
        }
        for item in data.assumptions:
            key = item.get("key", "")
            name = item.get("name", key)
            logic = str(item.get("logic", "")).strip()
            source_ref = str(item.get("source_ref", "")).strip()
            status = "OK"
            details = []
            if _is_rate_like(str(key), str(name)) and not logic:
                status = "CHECK"
                details.append("rate/share/ratio missing logic")
            if source_ref and source_ids and source_ref not in source_ids:
                status = "CHECK"
                details.append(f"unknown source_ref {source_ref}")
            if not source_ref and not logic:
                status = "CHECK"
                details.append("missing source_ref and logic")
            ws.cell(row, 1, f"Assumption {key}")
            ws.cell(row, 2, status)
            ws.cell(row, 3, "; ".join(details) if details else "Traceable")
            _style_row(ws, row, 3, styles)
            row += 1

        _set_widths(ws, [30, 14, 70])


class _Styles:
    def __init__(self) -> None:
        self.title = Font(bold=True, size=14, color="1F4E79")
        self.subtitle = Font(bold=True, size=11, color="1F4E79")
        self.header_fill = PatternFill("solid", fgColor="1F4E79")
        self.header_font = Font(bold=True, color="FFFFFF")
        self.input_fill = PatternFill("solid", fgColor="FFF2CC")
        self.formula_fill = PatternFill("solid", fgColor="E2F0D9")
        self.border = Border(
            left=Side(style="thin", color="D9E2F3"),
            right=Side(style="thin", color="D9E2F3"),
            top=Side(style="thin", color="D9E2F3"),
            bottom=Side(style="thin", color="D9E2F3"),
        )


def _write_header(ws, row: int, headers: List[str], styles: _Styles) -> None:
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row, col, header)
        cell.fill = styles.header_fill
        cell.font = styles.header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = styles.border


def _style_row(ws, row: int, cols: int, styles: _Styles) -> None:
    for col in range(1, cols + 1):
        cell = ws.cell(row, col)
        cell.border = styles.border
        cell.alignment = Alignment(vertical="top", wrap_text=True)


def _write_formula_rows(ws, rows: List[Tuple[str, str, str, str, str]], styles: _Styles) -> int:
    row_idx = 4
    for label, logic, formula, unit, note in rows:
        ws.cell(row_idx, 1, label)
        ws.cell(row_idx, 2, logic)
        ws.cell(row_idx, 3, formula)
        ws.cell(row_idx, 4, unit)
        ws.cell(row_idx, 5, note)
        ws.cell(row_idx, 3).fill = styles.formula_fill
        ws.cell(row_idx, 3).number_format = "#,##0.00"
        _style_row(ws, row_idx, 5, styles)
        row_idx += 1
    return row_idx - 1


def _set_widths(ws, widths: List[int]) -> None:
    for idx, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = width


def _replace_formula_tokens(formula: str, key_map: Dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in key_map:
            raise ValueError(f"Unknown assumption key in formula: {key}")
        return key_map[key]

    return re.sub(r"\{([A-Za-z0-9_\-.]+)\}", repl, formula)


def _sheet_cell(sheet_name: str, cell: str) -> str:
    escaped = sheet_name.replace("'", "''")
    return f"'{escaped}'!{cell}"


def _annual_values(data: MarketSizingData) -> List[Tuple[int, float, float, float]]:
    rows = []
    sam_ratio = _assumption_numeric(data, "sam_ratio", data.sam / data.tam if data.tam else 0)
    som_share = _assumption_numeric(data, "som_share", data.som / data.sam if data.sam else 0)
    for offset in range(data.forecast_years):
        if data.market_segments:
            tam = sum(values[offset] for _, values in _segment_values(data))
        else:
            tam = data.tam * ((1 + data.cagr) ** offset)
        sam = tam * sam_ratio
        som = sam * som_share
        rows.append((data.base_year + offset, tam, sam, som))
    return rows


def _segment_values(data: MarketSizingData) -> List[Tuple[str, List[float]]]:
    rows = []
    for segment in data.market_segments:
        base_value = float(segment.get("base_value", 0))
        growth_rate = float(segment.get("growth_rate", data.cagr))
        values = [base_value * ((1 + growth_rate) ** offset) for offset in range(data.forecast_years)]
        rows.append((str(segment.get("name", "")), values))
    return rows


def _assumption_numeric(data: MarketSizingData, key: str, default: float) -> float:
    for item in data.assumptions:
        if str(item.get("key", "")).strip() == key:
            try:
                return float(item.get("numeric_value"))
            except (TypeError, ValueError):
                return default
    return default


def _is_rate_like(key: str, name: str) -> bool:
    haystack = f"{key} {name}".lower()
    return any(word in haystack for word in RATE_KEYWORDS)


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", value.strip())
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned[:80] or "market"


if __name__ == "__main__":
    demo = MarketSizingData(
        market_name="示例新兴服务市场",
        geography="中国大陆",
        base_year=2026,
        forecast_years=5,
        tam=9.6,
        sam=5.8,
        som=0.3,
        unit="亿元",
        cagr=0.08,
        core_insight="示例模型用于演示公式链和核心结论页，不代表真实市场结论。",
        market_segments=[
            {"name": "核心场景 A", "base_value": 6.0, "growth_rate": 0.10, "logic": "对象数、渗透率和年费相乘得到。"},
            {"name": "验证场景 B", "base_value": 3.6, "growth_rate": 0.05, "logic": "由相邻场景 proxy 推导。"},
        ],
        assumptions=[
            {"key": "base_pop", "name": "基础人口", "numeric_value": 1.0, "unit": "亿人", "logic": "目标城市人口换算。"},
            {"key": "core_pop_pct", "name": "核心人群占比", "numeric_value": 0.40, "unit": "%", "logic": "年龄、收入和场景筛选。"},
            {"key": "pene_rate", "name": "付费渗透率", "numeric_value": 0.20, "unit": "%", "logic": "参考相邻市场 40%，因教育成本和替代品冲击折半。"},
            {"key": "freq", "name": "年购买频次", "numeric_value": 12, "unit": "次/年", "logic": "按月度订阅处理。"},
            {"key": "price", "name": "单次价格", "numeric_value": 100, "unit": "元", "logic": "公开价格带中位数。"},
            {"key": "sam_ratio", "name": "可服务比例", "numeric_value": 0.60, "unit": "%", "logic": "扣除不可服务地域、渠道和客户。"},
            {"key": "som_share", "name": "年度可获取份额", "numeric_value": 0.05, "unit": "%", "logic": "按销售产能、竞品份额和进入节奏估算。"},
            {"key": "cagr", "name": "年增长率", "numeric_value": 0.08, "unit": "%", "logic": "用户增长、价格变化和渗透率提升合成。"},
        ],
    )
    generated = ReportGenerator().generate(demo, Path(__file__).parent.parent / "output", ["xlsx", "md"])
    for kind, path in generated.items():
        print(f"{kind}: {path}")
