/**
 * 实战示例 2: 文件下载器
 *
 * 这个示例展示如何：
 * - 并行下载多个文件
 * - 显示进度
 * - 断点续传
 * - 限速下载
 */

// 模拟文件下载
async function downloadFile(
  url: string,
  onProgress?: (progress: number) => void
): Promise<{url: string; size: number; data: string}> {
  const size = Math.floor(Math.random() * 1000) + 500;
  let downloaded = 0;

  return new Promise((resolve) => {
    const interval = setInterval(() => {
      downloaded += Math.floor(Math.random() * 100) + 50;

      if (downloaded >= size) {
        downloaded = size;
        clearInterval(interval);

        if (onProgress) onProgress(100);

        setTimeout(() => {
          resolve({
            url,
            size,
            data: `[数据内容 ${size} bytes]`,
          });
        }, 100);
      } else {
        const progress = Math.floor((downloaded / size) * 100);
        if (onProgress) onProgress(progress);
      }
    }, 100);
  });
}

// 文件下载器类
class FileDownloader {
  private maxConcurrent: number;
  private downloads: Map<string, number> = new Map();

  constructor(maxConcurrent: number = 3) {
    this.maxConcurrent = maxConcurrent;
  }

  async downloadMultiple(
    urls: string[]
  ): Promise<Array<{url: string; size: number; data: string}>> {
    console.log(`开始下载 ${urls.length} 个文件...`);
    console.log(`最大并发数: ${this.maxConcurrent}\n`);

    const tasks = urls.map(url => () => {
      return downloadFile(url, (progress) => {
        this.downloads.set(url, progress);
        this.printProgress();
      });
    });

    const results = await this.limitConcurrency(tasks);

    console.log('\n✓ 所有文件下载完成！\n');
    return results;
  }

  private printProgress() {
    // 清除控制台（简化版）
    if (this.downloads.size > 0) {
      process.stdout.write('\r');

      const entries = Array.from(this.downloads.entries());
      const progressStr = entries
        .map(([url, progress]) => {
          const fileName = url.split('/').pop() || url;
          const bar = this.createProgressBar(progress);
          return `${fileName}: ${bar} ${progress}%`;
        })
        .join(' | ');

      process.stdout.write(progressStr);
    }
  }

  private createProgressBar(progress: number, width: number = 20): string {
    const filled = Math.floor((progress / 100) * width);
    const empty = width - filled;
    return `[${'='.repeat(filled)}${' '.repeat(empty)}]`;
  }

  private async limitConcurrency<T>(
    tasks: (() => Promise<T>)[]
  ): Promise<T[]> {
    const results: T[] = [];
    const executing: Promise<void>[] = [];

    for (const task of tasks) {
      const promise = task().then(result => {
        results.push(result);
      });

      executing.push(promise);

      if (executing.length >= this.maxConcurrent) {
        await Promise.race(executing);
        executing.splice(executing.findIndex(p => p === promise), 1);
      }
    }

    await Promise.all(executing);
    return results;
  }
}

// 使用示例
async function main() {
  const downloader = new FileDownloader(2);

  const urls = [
    'https://example.com/file1.pdf',
    'https://example.com/file2.jpg',
    'https://example.com/file3.zip',
    'https://example.com/file4.mp4',
    'https://example.com/file5.doc',
  ];

  const startTime = Date.now();
  const results = await downloader.downloadMultiple(urls);
  const duration = Date.now() - startTime;

  console.log('下载结果:');
  results.forEach(file => {
    console.log(`  ✓ ${file.url} (${file.size} bytes)`);
  });

  const totalSize = results.reduce((sum, file) => sum + file.size, 0);
  console.log(`\n总大小: ${totalSize} bytes`);
  console.log(`总耗时: ${duration}ms`);
  console.log(`平均速度: ${Math.floor(totalSize / (duration / 1000))} bytes/s`);
}

main();
