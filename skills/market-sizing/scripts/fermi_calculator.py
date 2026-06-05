"""
Fermi Calculator
================

Fermi 估算计算引擎，支持多种分解模式：
1. 人口基数法: 总人口 → 目标人群占比 → 渗透率 → 客单价
2. 机构基数法: 目标机构数 → 采用率 → 每机构用量 × 单价
3. 替代法: 现有解决方案市场 × 替代率
4. 价值链法: 终端产品市场 × 该环节价值占比
5. 频率法: 目标用户数 × 使用频率 × 单次价值

使用方法:
    from fermi_calculator import FermiCalculator
    
    calc = FermiCalculator()
    result = calc.population_based(
        base_population=1.4e9,
        filters=[("城市人口", 0.65), ("20-40岁", 0.30), ("咖啡饮用者", 0.15)],
        penetration_rate=0.5,
        average_spend=50,
        frequency=52  # 周均消费次数
    )
    print(result)
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Callable
import math


@dataclass
class FermiResult:
    """Fermi 估算结果"""
    value: float                          # 最终估算值
    unit: str                             # 单位
    steps: List[Tuple[str, float, str]]   # 计算步骤 [(描述, 值, 依据)]
    formula: str                          # 计算公式
    method: str                           # 使用的方法
    assumptions: List[Tuple[str, float, str]]  # 假设列表 [(假设名, 值, 来源)]
    
    def __str__(self) -> str:
        lines = [f"== Fermi 估算结果 =="]
        lines.append(f"方法: {self.method}")
        lines.append(f"结果: {self._format_number(self.value)} {self.unit}")
        lines.append(f"\n公式: {self.formula}")
        lines.append(f"\n计算步骤:")
        for i, (desc, val, basis) in enumerate(self.steps, 1):
            lines.append(f"  {i}. {desc}: {self._format_number(val)} ({basis})")
        lines.append(f"\n关键假设:")
        for name, val, source in self.assumptions:
            lines.append(f"  - {name}: {val} (来源: {source})")
        return "\n".join(lines)
    
    @staticmethod
    def _format_number(n: float) -> str:
        """格式化大数字"""
        if n >= 1e12:
            return f"{n/1e12:.2f} 万亿"
        elif n >= 1e8:
            return f"{n/1e8:.2f} 亿"
        elif n >= 1e4:
            return f"{n/1e4:.2f} 万"
        else:
            return f"{n:.2f}"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "value": self.value,
            "unit": self.unit,
            "steps": self.steps,
            "formula": self.formula,
            "method": self.method,
            "assumptions": self.assumptions,
        }


class FermiCalculator:
    """
    Fermi 估算计算器
    
    Example:
        >>> calc = FermiCalculator()
        >>> result = calc.population_based(
        ...     base_population=1.4e9,
        ...     filters=[("城市人口", 0.65), ("咖啡饮用者", 0.15)],
        ...     penetration_rate=1.0,
        ...     average_spend=30,
        ...     frequency=100
        ... )
        >>> print(result)
    """
    
    def population_based(
        self,
        base_population: float,
        filters: List[Tuple[str, float]],
        penetration_rate: float,
        average_spend: float,
        frequency: int = 1,
        unit: str = "元",
        assumptions_sources: Optional[dict] = None
    ) -> FermiResult:
        """
        人口基数法
        
        公式: 基数 × 各层筛选率 × 渗透率 × 客单价 × 频率
        
        Args:
            base_population: 基础人口数
            filters: 筛选条件列表 [(条件名, 占比), ...]
            penetration_rate: 目标产品/服务渗透率
            average_spend: 平均消费金额
            frequency: 年消费频率 (默认 1)
            unit: 金额单位
            assumptions_sources: 假设来源 {假设名: 来源}
        """
        assumptions_sources = assumptions_sources or {}
        steps = []
        assumptions = []
        
        # 输入校验
        if base_population <= 0:
            raise ValueError(f"base_population 必须为正数，当前值: {base_population}")
        if not 0 < penetration_rate <= 1:
            raise ValueError(f"penetration_rate 必须在 (0, 1] 范围内，当前值: {penetration_rate}")
        if average_spend <= 0:
            raise ValueError(f"average_spend 必须为正数，当前值: {average_spend}")
        if frequency <= 0:
            raise ValueError(f"frequency 必须为正数，当前值: {frequency}")
        for name, rate in filters:
            if not 0 < rate <= 1:
                raise ValueError(f"筛选条件 '{name}' 的占比必须在 (0, 1] 范围内，当前值: {rate}")
        
        # Step 1: 基础人口
        current = base_population
        steps.append(("基础人口", current, "基数"))
        assumptions.append(("基础人口", base_population, assumptions_sources.get("基础人口", "统计局/估算")))
        
        # Step 2: 各层筛选
        for name, rate in filters:
            current = current * rate
            steps.append((f"筛选: {name} ({rate*100:.1f}%)", current, f"剩余 {self._format_number(current)} 人"))
            assumptions.append((name, rate, assumptions_sources.get(name, "估算")))
        
        # Step 3: 渗透率
        target_users = current * penetration_rate
        steps.append((f"渗透率 ({penetration_rate*100:.1f}%)", target_users, f"目标用户 {self._format_number(target_users)} 人"))
        assumptions.append(("渗透率", penetration_rate, assumptions_sources.get("渗透率", "估算")))
        
        # Step 4: 消费频率和客单价
        total_value = target_users * average_spend * frequency
        steps.append((f"年消费 (客单价 {average_spend}{unit} × 频率 {frequency})", total_value, "年市场规模"))
        assumptions.append(("客单价", average_spend, assumptions_sources.get("客单价", "市场调研")))
        assumptions.append(("年消费频率", frequency, assumptions_sources.get("频率", "估算")))
        
        # 构建公式
        filter_str = " × ".join([f"{name}({rate})" for name, rate in filters])
        formula = f"基数 × {filter_str} × 渗透率 × 客单价 × 频率"
        
        return FermiResult(
            value=total_value,
            unit=unit,
            steps=steps,
            formula=formula,
            method="人口基数法",
            assumptions=assumptions
        )
    
    def institution_based(
        self,
        institution_count: float,
        adoption_rate: float,
        units_per_institution: float,
        price_per_unit: float,
        unit: str = "元",
        assumptions_sources: Optional[dict] = None
    ) -> FermiResult:
        """
        机构基数法
        
        公式: 目标机构数 × 采用率 × 每机构用量 × 单价
        
        Args:
            institution_count: 目标机构数量
            adoption_rate: 采用率
            units_per_institution: 每个机构的用量
            price_per_unit: 单位价格
        """
        assumptions_sources = assumptions_sources or {}
        steps = []
        assumptions = []
        
        # 输入校验
        if institution_count <= 0:
            raise ValueError(f"institution_count 必须为正数，当前值: {institution_count}")
        if not 0 < adoption_rate <= 1:
            raise ValueError(f"adoption_rate 必须在 (0, 1] 范围内，当前值: {adoption_rate}")
        if units_per_institution <= 0:
            raise ValueError(f"units_per_institution 必须为正数，当前值: {units_per_institution}")
        if price_per_unit <= 0:
            raise ValueError(f"price_per_unit 必须为正数，当前值: {price_per_unit}")
        
        # Step 1: 机构数
        steps.append(("目标机构数", institution_count, "基数"))
        assumptions.append(("机构数量", institution_count, assumptions_sources.get("机构数量", "工商数据")))
        
        # Step 2: 采用率
        adopters = institution_count * adoption_rate
        steps.append((f"采用率 ({adoption_rate*100:.1f}%)", adopters, f"{self._format_number(adopters)} 机构"))
        assumptions.append(("采用率", adoption_rate, assumptions_sources.get("采用率", "行业报告")))
        
        # Step 3: 每机构用量
        total_units = adopters * units_per_institution
        steps.append((f"每机构用量 ({units_per_institution})", total_units, f"总用量 {self._format_number(total_units)}"))
        assumptions.append(("每机构用量", units_per_institution, assumptions_sources.get("每机构用量", "估算")))
        
        # Step 4: 单价
        total_value = total_units * price_per_unit
        steps.append((f"单价 ({price_per_unit} {unit})", total_value, "市场规模"))
        assumptions.append(("单价", price_per_unit, assumptions_sources.get("单价", "市场调研")))
        
        formula = "机构数 × 采用率 × 每机构用量 × 单价"
        
        return FermiResult(
            value=total_value,
            unit=unit,
            steps=steps,
            formula=formula,
            method="机构基数法",
            assumptions=assumptions
        )
    
    def substitution_based(
        self,
        existing_market_size: float,
        substitution_rate: float,
        price_premium: float = 1.0,
        unit: str = "元",
        assumptions_sources: Optional[dict] = None
    ) -> FermiResult:
        """
        替代法
        
        公式: 现有市场规模 × 替代率 × 价格系数
        
        适用于: 新产品替代现有解决方案的场景
        
        Args:
            existing_market_size: 现有解决方案的市场规模
            substitution_rate: 预期替代率
            price_premium: 价格系数 (>1 表示溢价, <1 表示折价)
        """
        assumptions_sources = assumptions_sources or {}
        steps = []
        assumptions = []
        
        steps.append(("现有市场规模", existing_market_size, "基数"))
        assumptions.append(("现有市场", existing_market_size, assumptions_sources.get("现有市场", "行业报告")))
        
        substituted = existing_market_size * substitution_rate
        steps.append((f"替代率 ({substitution_rate*100:.1f}%)", substituted, "可替代市场"))
        assumptions.append(("替代率", substitution_rate, assumptions_sources.get("替代率", "技术分析")))
        
        total_value = substituted * price_premium
        if price_premium != 1.0:
            steps.append((f"价格系数 ({price_premium}x)", total_value, "市场规模"))
            assumptions.append(("价格系数", price_premium, assumptions_sources.get("价格系数", "定价策略")))
        
        formula = "现有市场 × 替代率" + (f" × 价格系数({price_premium})" if price_premium != 1.0 else "")
        
        return FermiResult(
            value=total_value,
            unit=unit,
            steps=steps,
            formula=formula,
            method="替代法",
            assumptions=assumptions
        )
    
    def value_chain_based(
        self,
        end_market_size: float,
        value_share: float,
        unit: str = "元",
        assumptions_sources: Optional[dict] = None
    ) -> FermiResult:
        """
        价值链法
        
        公式: 终端市场规模 × 该环节价值占比
        
        适用于: 估算产业链中某个环节的市场规模
        
        Args:
            end_market_size: 终端产品/服务的市场规模
            value_share: 该环节在价值链中的占比
        """
        assumptions_sources = assumptions_sources or {}
        steps = []
        assumptions = []
        
        steps.append(("终端市场规模", end_market_size, "下游市场"))
        assumptions.append(("终端市场", end_market_size, assumptions_sources.get("终端市场", "行业报告")))
        
        total_value = end_market_size * value_share
        steps.append((f"价值链占比 ({value_share*100:.1f}%)", total_value, "本环节市场"))
        assumptions.append(("价值链占比", value_share, assumptions_sources.get("价值链占比", "产业分析")))
        
        formula = "终端市场 × 价值链占比"
        
        return FermiResult(
            value=total_value,
            unit=unit,
            steps=steps,
            formula=formula,
            method="价值链法",
            assumptions=assumptions
        )
    
    def value_based(
        self,
        target_count: float,
        problem_frequency: float,
        problem_cost: float,
        willingness_to_pay_ratio: float,
        unit: str = "元",
        assumptions_sources: Optional[dict] = None
    ) -> FermiResult:
        """
        价值基础法 (Value-Based)
        
        公式: 目标客户数 × 问题发生频率 × 问题成本 × 愿付比例
        
        适用于: 无法直接获取市场数据，需要从解决问题的价值反推
        
        Args:
            target_count: 目标客户数量
            problem_frequency: 问题年均发生频率
            problem_cost: 每次问题的成本
            willingness_to_pay_ratio: 客户愿意为解决方案支付的比例
        """
        assumptions_sources = assumptions_sources or {}
        steps = []
        assumptions = []
        
        steps.append(("目标客户数", target_count, "基数"))
        assumptions.append(("目标客户", target_count, assumptions_sources.get("目标客户", "市场调研")))
        
        annual_problem_value = target_count * problem_frequency * problem_cost
        steps.append((f"问题总成本 (频率 {problem_frequency} × 成本 {problem_cost})", annual_problem_value, "可解决的价值"))
        assumptions.append(("问题频率", problem_frequency, assumptions_sources.get("问题频率", "客户调研")))
        assumptions.append(("问题成本", problem_cost, assumptions_sources.get("问题成本", "财务数据")))
        
        total_value = annual_problem_value * willingness_to_pay_ratio
        steps.append((f"愿付比例 ({willingness_to_pay_ratio*100:.1f}%)", total_value, "市场规模"))
        assumptions.append(("愿付比例", willingness_to_pay_ratio, assumptions_sources.get("愿付比例", "定价调研")))
        
        formula = "目标客户 × 问题频率 × 问题成本 × 愿付比例"
        
        return FermiResult(
            value=total_value,
            unit=unit,
            steps=steps,
            formula=formula,
            method="价值基础法",
            assumptions=assumptions
        )
    
    def custom(
        self,
        formula_fn: Callable[..., float],
        inputs: dict,
        method_name: str = "自定义方法",
        unit: str = "元",
        assumptions_sources: Optional[dict] = None
    ) -> FermiResult:
        """
        自定义 Fermi 估算
        
        Args:
            formula_fn: 计算函数，接收 inputs 作为关键字参数
            inputs: 输入参数字典 {参数名: 值}
            method_name: 方法名称
        """
        assumptions_sources = assumptions_sources or {}
        
        result = formula_fn(**inputs)
        
        steps = []
        assumptions = []
        for name, value in inputs.items():
            steps.append((name, value, "输入"))
            assumptions.append((name, value, assumptions_sources.get(name, "用户输入")))
        steps.append(("计算结果", result, "输出"))
        
        return FermiResult(
            value=result,
            unit=unit,
            steps=steps,
            formula=method_name,
            method=method_name,
            assumptions=assumptions
        )
    
    @staticmethod
    def _format_number(n: float) -> str:
        """格式化数字"""
        if n >= 1e8:
            return f"{n/1e8:.2f}亿"
        elif n >= 1e4:
            return f"{n/1e4:.2f}万"
        else:
            return f"{n:.0f}"


# 便捷函数
def fermi_estimate(**kwargs) -> FermiResult:
    """
    快速 Fermi 估算 (自动选择方法)
    
    根据提供的参数自动选择最合适的方法
    """
    calc = FermiCalculator()
    
    if "base_population" in kwargs:
        return calc.population_based(**kwargs)
    elif "institution_count" in kwargs:
        return calc.institution_based(**kwargs)
    elif "existing_market_size" in kwargs:
        return calc.substitution_based(**kwargs)
    elif "end_market_size" in kwargs:
        return calc.value_chain_based(**kwargs)
    elif "problem_cost" in kwargs:
        return calc.value_based(**kwargs)
    else:
        raise ValueError("无法确定使用哪种 Fermi 方法，请明确提供方法所需参数")


if __name__ == "__main__":
    # 示例: 中国咖啡市场规模估算
    calc = FermiCalculator()
    
    result = calc.population_based(
        base_population=1.4e9,
        filters=[
            ("城市人口", 0.65),
            ("20-50岁", 0.45),
            ("咖啡饮用者", 0.20),
        ],
        penetration_rate=1.0,
        average_spend=25,
        frequency=100,  # 年均消费 100 杯
        unit="元"
    )
    
    print(result)
    print(f"\n市场规模约: {result.value / 1e8:.0f} 亿元")
