# Week 7-1: Code Reviews: Just Do It
# 代码审查：去做就是了

> **Original Link**: [https://blog.codinghorror.com/code-reviews-just-do-it/](https://blog.codinghorror.com/code-reviews-just-do-it/)
> **Title**: Code Reviews: Just Do It
> **Author**: Jeff Atwood
> **Week**: 7
> **Reading Time**: 5 min
> **Priority**: High
> **Translation Date**: 2026-02-03

---

在 [Humanizing Peer Reviews](https://web.archive.org/web/20060315135514/http://www.processimpact.com/articles/humanizing_reviews.html) 一文中，Karl Wiegers 以一句强有力的断言开篇：

> 同行评审（Peer review）——即由软件交付物的作者以外的人对其进行检查，以发现缺陷和改进机会的活动——是目前可用的最强大的软件质量工具之一。同行评审的方法包括审查（inspections）、走查（walkthroughs）、同行桌面检查（peer deskchecks）以及其他类似的活动。

在 Vertigo 参与了一段时间的代码审查后，我相信 **同行代码审查是你为提高代码质量所能做的最重要的一件事**。如果你现在还没有和其他开发者一起做代码审查，那么你正在遗漏代码中的大量 Bug，并且欺骗自己失去了许多关键的职业发展机会。就我而言，只有当我与另一位开发者一起检查过我的代码后，代码才算完成。

但不要只听我的一面之词。McConnell 在 [Code Complete](http://www.amazon.com/exec/obidos/ASIN/0735619670) 中提供了大量证据证明代码审查的有效性：

> ……仅靠软件测试的有效性是有限的——单元测试的平均缺陷检出率仅为 25%，功能测试为 35%，集成测试为 45%。相比之下，**设计和代码审查的平均有效性分别为 55% 和 60%**。审查结果的案例研究令人印象深刻：
>
> - 在一个软件维护组织中，引入代码审查之前，55% 的单行维护更改是错误的。引入审查后，只有 2% 的更改是错误的。如果考虑到所有更改，引入审查后，95% 的更改第一次就是正确的。而在引入审查之前，只有不到 20% 的更改第一次是正确的。
> - 在同一组人开发的 11 个程序中，前 5 个是在没有审查的情况下开发的。其余 6 个是在有审查的情况下开发的。所有程序发布到生产环境后，前 5 个程序平均每 100 行代码有 4.5 个错误。而后 6 个经过审查的程序平均每 100 行代码只有 0.82 个错误。审查将错误减少了 80% 以上。
> - Aetna 保险公司通过使用审查发现了程序中 82% 的错误，并使其开发资源减少了 20%。
> - IBM 的 50 万行 Orbit 项目使用了 11 级审查。它提前交付，并且只有通常预期错误的 1% 左右。
> - 在 AT&T 的一个拥有 200 多人的组织中进行的一项研究报告称，在引入审查后，该组织的生产率提高了 14%，缺陷减少了 90%。
> - 喷气推进实验室（JPL）估计，通过在早期阶段发现并修复缺陷，每一次审查大约能节省 25,000 美元。

代码审查的唯一障碍是找到一位你尊重的开发者来做这件事，并腾出时间来进行审查。一旦你开始，我想你会很快发现，**你在代码审查上花费的每一分钟都会得到十倍的回报**。

如果你的组织刚开始接触代码审查，我强烈推荐 Karl 的书 [Peer Reviews in Software](http://www.amazon.com/exec/obidos/ASIN/0201734850): A Practical Guide。Karl 在他的网站上提供的 [样章](https://web.archive.org/web/20060315135046/http://www.processimpact.com/reviews_book/reviews_book_toc.shtml) 也是很好的入门指南。
