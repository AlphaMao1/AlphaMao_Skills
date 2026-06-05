"""
Monte Carlo Simulation for Market Sizing
=========================================

用于处理市场规模估算中的不确定性：
- 支持多种概率分布
- 输出置信区间而非单点估计
- 敏感性分析 (Tornado Chart)

使用方法:
    from monte_carlo import MonteCarloSimulator, Assumption
    
    sim = MonteCarloSimulator()
    
    result = sim.run(
        assumptions={
            "市场基数": Assumption(min=800, max=1200, most_likely=1000, distribution="triangular"),
            "渗透率": Assumption(min=0.15, max=0.35, most_likely=0.25, distribution="triangular"),
            "客单价": Assumption(min=30, max=50, most_likely=40, distribution="triangular"),
        },
        formula=lambda 市场基数, 渗透率, 客单价: 市场基数 * 渗透率 * 客单价,
        n_simulations=10000
    )
    
    print(result)
"""

from dataclasses import dataclass
from typing import Dict, Callable, List, Tuple, Optional, Literal
from collections import OrderedDict

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

if not NUMPY_AVAILABLE:
    raise ImportError(
        "Monte Carlo 模拟需要 numpy。请安装: pip install numpy\n"
        "如果不需要 Monte Carlo 功能，可以只使用 fermi_calculator.py"
    )


DistributionType = Literal["uniform", "triangular", "normal", "lognormal"]


@dataclass
class Assumption:
    """
    单个假设的定义
    
    Attributes:
        min: 最小值
        max: 最大值
        most_likely: 最可能值 (用于 triangular 分布)
        distribution: 分布类型
        unit: 单位 (可选)
        source: 数据来源 (可选)
    """
    min: float
    max: float
    most_likely: Optional[float] = None
    distribution: DistributionType = "triangular"
    unit: str = ""
    source: str = ""
    
    def __post_init__(self):
        if self.most_likely is None:
            self.most_likely = (self.min + self.max) / 2
        
        # 验证
        if self.min > self.max:
            raise ValueError(f"min ({self.min}) 不能大于 max ({self.max})")
        if not (self.min <= self.most_likely <= self.max):
            raise ValueError(f"most_likely ({self.most_likely}) 必须在 [{self.min}, {self.max}] 范围内")


@dataclass
class MonteCarloResult:
    """Monte Carlo 模拟结果"""
    mean: float                           # 均值
    median: float                         # 中位数
    std: float                            # 标准差
    p5: float                             # 5% 分位数
    p10: float                            # 10% 分位数
    p25: float                            # 25% 分位数
    p75: float                            # 75% 分位数
    p90: float                            # 90% 分位数
    p95: float                            # 95% 分位数
    min: float                            # 最小值
    max: float                            # 最大值
    n_simulations: int                    # 模拟次数
    raw_results: np.ndarray               # 原始结果 (用于绘图)
    sensitivity: Dict[str, float]         # 敏感性分析结果
    unit: str                             # 单位
    
    def __str__(self) -> str:
        lines = [
            "="*50,
            "Monte Carlo 模拟结果",
            "="*50,
            f"模拟次数: {self.n_simulations:,}",
            "",
            "📊 汇总统计:",
            f"  均值:   {self._format(self.mean)} {self.unit}",
            f"  中位数: {self._format(self.median)} {self.unit}",
            f"  标准差: {self._format(self.std)} {self.unit}",
            "",
            "📈 置信区间:",
            f"  90% CI: [{self._format(self.p5)}, {self._format(self.p95)}] {self.unit}",
            f"  80% CI: [{self._format(self.p10)}, {self._format(self.p90)}] {self.unit}",
            f"  50% CI: [{self._format(self.p25)}, {self._format(self.p75)}] {self.unit}",
            "",
            f"  范围:   [{self._format(self.min)}, {self._format(self.max)}] {self.unit}",
        ]
        
        if self.sensitivity:
            lines.append("")
            lines.append("🌪️ 敏感性分析 (Tornado):")
            sorted_sens = sorted(self.sensitivity.items(), key=lambda x: abs(x[1]), reverse=True)
            for name, impact in sorted_sens:
                bar_len = int(abs(impact) / max(abs(v) for v in self.sensitivity.values()) * 20)
                bar = "█" * bar_len
                lines.append(f"  {name}: {bar} ({impact:+.1f}%)")
        
        return "\n".join(lines)
    
    @staticmethod
    def _format(n: float) -> str:
        """格式化数字"""
        if n >= 1e12:
            return f"{n/1e12:.2f}万亿"
        elif n >= 1e8:
            return f"{n/1e8:.2f}亿"
        elif n >= 1e4:
            return f"{n/1e4:.2f}万"
        else:
            return f"{n:.2f}"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "mean": self.mean,
            "median": self.median,
            "std": self.std,
            "p5": self.p5,
            "p10": self.p10,
            "p25": self.p25,
            "p75": self.p75,
            "p90": self.p90,
            "p95": self.p95,
            "min": self.min,
            "max": self.max,
            "n_simulations": self.n_simulations,
            "sensitivity": self.sensitivity,
            "unit": self.unit,
        }
    
    def get_percentile(self, p: float) -> float:
        """获取任意分位数"""
        return float(np.percentile(self.raw_results, p))


class MonteCarloSimulator:
    """
    Monte Carlo 模拟器
    
    Example:
        >>> sim = MonteCarloSimulator(seed=42)
        >>> result = sim.run(
        ...     assumptions={
        ...         "用户数": Assumption(min=100000, max=200000, most_likely=150000),
        ...         "转化率": Assumption(min=0.01, max=0.05, most_likely=0.03),
        ...         "客单价": Assumption(min=100, max=200, most_likely=150),
        ...     },
        ...     formula=lambda 用户数, 转化率, 客单价: 用户数 * 转化率 * 客单价
        ... )
        >>> print(result)
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        初始化模拟器
        
        Args:
            seed: 随机种子 (用于可重复性)
        """
        self.rng = np.random.default_rng(seed)
    
    def _sample(self, assumption: Assumption, n: int) -> np.ndarray:
        """
        根据假设生成随机样本
        
        Args:
            assumption: 假设定义
            n: 样本数量
        """
        if assumption.distribution == "uniform":
            return self.rng.uniform(assumption.min, assumption.max, n)
        
        elif assumption.distribution == "triangular":
            return self.rng.triangular(
                assumption.min, 
                assumption.most_likely, 
                assumption.max, 
                n
            )
        
        elif assumption.distribution == "normal":
            # 使用 min/max 作为 ±2σ
            mean = assumption.most_likely
            std = (assumption.max - assumption.min) / 4
            samples = self.rng.normal(mean, std, n)
            # 裁剪到范围内
            return np.clip(samples, assumption.min, assumption.max)
        
        elif assumption.distribution == "lognormal":
            # 使用对数正态分布 (适合右偏数据，如收入)
            log_mean = np.log(assumption.most_likely)
            log_std = (np.log(assumption.max) - np.log(assumption.min)) / 4
            samples = self.rng.lognormal(log_mean, log_std, n)
            return np.clip(samples, assumption.min, assumption.max)
        
        else:
            raise ValueError(f"未知分布类型: {assumption.distribution}")
    
    def run(
        self,
        assumptions: Dict[str, Assumption],
        formula: Callable[..., float],
        n_simulations: int = 10000,
        unit: str = "元",
        run_sensitivity: bool = True
    ) -> MonteCarloResult:
        """
        执行 Monte Carlo 模拟
        
        Args:
            assumptions: 假设字典 {假设名: Assumption}
            formula: 计算公式函数，参数名需与假设名对应
            n_simulations: 模拟次数
            unit: 结果单位
            run_sensitivity: 是否执行敏感性分析
            
        Returns:
            MonteCarloResult: 模拟结果
        """
        # 生成所有假设的样本
        samples = {}
        for name, assumption in assumptions.items():
            samples[name] = self._sample(assumption, n_simulations)
        
        # 计算每次模拟的结果
        results = np.zeros(n_simulations)
        for i in range(n_simulations):
            kwargs = {name: values[i] for name, values in samples.items()}
            results[i] = formula(**kwargs)
        
        # 敏感性分析
        sensitivity = {}
        if run_sensitivity:
            sensitivity = self._sensitivity_analysis(assumptions, formula)
        
        return MonteCarloResult(
            mean=float(np.mean(results)),
            median=float(np.median(results)),
            std=float(np.std(results)),
            p5=float(np.percentile(results, 5)),
            p10=float(np.percentile(results, 10)),
            p25=float(np.percentile(results, 25)),
            p75=float(np.percentile(results, 75)),
            p90=float(np.percentile(results, 90)),
            p95=float(np.percentile(results, 95)),
            min=float(np.min(results)),
            max=float(np.max(results)),
            n_simulations=n_simulations,
            raw_results=results,
            sensitivity=sensitivity,
            unit=unit,
        )
    
    def _sensitivity_analysis(
        self,
        assumptions: Dict[str, Assumption],
        formula: Callable[..., float]
    ) -> Dict[str, float]:
        """
        敏感性分析：计算每个假设变化对结果的影响
        
        原理：将每个假设从 most_likely 变化到 max，计算结果变化百分比
        """
        sensitivity = {}
        
        # 基准值：所有假设使用 most_likely
        base_kwargs = {name: a.most_likely for name, a in assumptions.items()}
        base_result = formula(**base_kwargs)
        
        if base_result == 0:
            return sensitivity
        
        # 每个假设单独变化
        for name, assumption in assumptions.items():
            # 从 most_likely 变化到 max
            test_kwargs = base_kwargs.copy()
            test_kwargs[name] = assumption.max
            high_result = formula(**test_kwargs)
            
            # 从 most_likely 变化到 min
            test_kwargs[name] = assumption.min
            low_result = formula(**test_kwargs)
            
            # 计算变化幅度 (取变化较大的那个)
            high_change = (high_result - base_result) / base_result * 100
            low_change = (low_result - base_result) / base_result * 100
            
            # 取绝对值较大的变化
            if abs(high_change) >= abs(low_change):
                sensitivity[name] = high_change
            else:
                sensitivity[name] = low_change
        
        return sensitivity


def quick_monte_carlo(
    assumptions: Dict[str, Tuple[float, float, float]],
    formula: Callable[..., float],
    n: int = 10000,
    unit: str = "元"
) -> MonteCarloResult:
    """
    快速 Monte Carlo 模拟 (简化接口)
    
    Args:
        assumptions: 简化的假设字典 {假设名: (min, most_likely, max)}
        formula: 计算公式
        n: 模拟次数
        unit: 单位
        
    Example:
        >>> result = quick_monte_carlo(
        ...     assumptions={
        ...         "用户数": (100000, 150000, 200000),
        ...         "转化率": (0.01, 0.03, 0.05),
        ...     },
        ...     formula=lambda 用户数, 转化率: 用户数 * 转化率
        ... )
    """
    full_assumptions = {
        name: Assumption(min=vals[0], most_likely=vals[1], max=vals[2])
        for name, vals in assumptions.items()
    }
    
    sim = MonteCarloSimulator()
    return sim.run(full_assumptions, formula, n, unit)


if __name__ == "__main__":
    # 示例：航空活塞发动机市场估算
    sim = MonteCarloSimulator(seed=42)
    
    result = sim.run(
        assumptions={
            "市场总规模(亿)": Assumption(min=20, max=35, most_likely=25.5, unit="亿元", source="IndexBox"),
            "200-500HP占比": Assumption(min=0.35, max=0.55, most_likely=0.45, source="机型分析"),
            "目标市占率": Assumption(min=0.10, max=0.20, most_likely=0.15, source="竞争分析"),
        },
        formula=lambda **kwargs: (
            kwargs["市场总规模(亿)"] * 
            kwargs["200-500HP占比"] * 
            kwargs["目标市占率"]
        ),
        n_simulations=10000,
        unit="亿元"
    )
    
    print(result)
