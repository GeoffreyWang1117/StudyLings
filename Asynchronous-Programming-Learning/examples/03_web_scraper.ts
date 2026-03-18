/**
 * 实战示例 3: 简单的网页爬虫
 *
 * 这个示例展示如何：
 * - 抓取网页数据
 * - 实现请求队列
 * - 遵守爬虫礼仪（延迟、限速）
 * - 去重和缓存
 */

// 模拟网页抓取
async function fetchPage(url: string): Promise<{
  url: string;
  title: string;
  links: string[];
}> {
  return new Promise((resolve) => {
    setTimeout(() => {
      const id = url.split('/').pop() || '0';
      resolve({
        url,
        title: `页面 ${id}`,
        links: [
          `https://example.com/page-${parseInt(id) + 1}`,
          `https://example.com/page-${parseInt(id) + 2}`,
        ],
      });
    }, Math.random() * 300 + 200);
  });
}

// 简单的爬虫类
class WebScraper {
  private visited: Set<string> = new Set();
  private queue: string[] = [];
  private maxDepth: number;
  private maxPages: number;
  private delay: number;
  private cache: Map<string, any> = new Map();

  constructor(options: {
    maxDepth?: number;
    maxPages?: number;
    delay?: number;
  } = {}) {
    this.maxDepth = options.maxDepth || 2;
    this.maxPages = options.maxPages || 10;
    this.delay = options.delay || 500; // 爬虫礼仪：500ms 延迟
  }

  async crawl(startUrl: string): Promise<Map<string, any>> {
    console.log(`开始爬取: ${startUrl}`);
    console.log(`最大深度: ${this.maxDepth}`);
    console.log(`最大页面数: ${this.maxPages}`);
    console.log(`请求延迟: ${this.delay}ms\n`);

    this.queue.push(startUrl);

    let depth = 0;

    while (this.queue.length > 0 && depth < this.maxDepth) {
      console.log(`\n深度 ${depth + 1}:`);

      const currentLevelUrls = [...this.queue];
      this.queue = [];

      for (const url of currentLevelUrls) {
        if (this.visited.size >= this.maxPages) {
          console.log('\n达到最大页面数限制');
          return this.cache;
        }

        if (this.visited.has(url)) {
          continue;
        }

        await this.crawlPage(url);

        // 遵守爬虫礼仪：请求之间延迟
        await new Promise(r => setTimeout(r, this.delay));
      }

      depth++;
    }

    console.log(`\n爬取完成！`);
    return this.cache;
  }

  private async crawlPage(url: string): Promise<void> {
    try {
      console.log(`  抓取: ${url}`);

      const page = await fetchPage(url);

      this.visited.add(url);
      this.cache.set(url, {
        title: page.title,
        links: page.links,
        scrapedAt: new Date(),
      });

      console.log(`    ✓ ${page.title} (发现 ${page.links.length} 个链接)`);

      // 将新链接加入队列
      for (const link of page.links) {
        if (!this.visited.has(link) && !this.queue.includes(link)) {
          this.queue.push(link);
        }
      }
    } catch (error: any) {
      console.log(`    ✗ 失败: ${error.message}`);
    }
  }

  getStats() {
    return {
      totalPages: this.visited.size,
      uniqueLinks: new Set(
        Array.from(this.cache.values()).flatMap((page: any) => page.links)
      ).size,
      cached: this.cache.size,
    };
  }
}

// 使用示例
async function main() {
  const scraper = new WebScraper({
    maxDepth: 3,
    maxPages: 15,
    delay: 300,
  });

  const startTime = Date.now();
  const results = await scraper.crawl('https://example.com/page-1');
  const duration = Date.now() - startTime;

  console.log('\n' + '='.repeat(50));
  console.log('爬取统计');
  console.log('='.repeat(50));

  const stats = scraper.getStats();
  console.log(`抓取页面: ${stats.totalPages}`);
  console.log(`发现链接: ${stats.uniqueLinks}`);
  console.log(`缓存条目: ${stats.cached}`);
  console.log(`总耗时: ${duration}ms`);

  console.log('\n缓存内容:');
  results.forEach((data, url) => {
    console.log(`\n${url}:`);
    console.log(`  标题: ${data.title}`);
    console.log(`  链接数: ${data.links.length}`);
  });
}

main();
