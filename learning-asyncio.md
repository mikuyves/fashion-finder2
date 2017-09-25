Asyncio - async / await
===

现在还是一知半解，但是经过实践还是摸索了一些可行的方法。
网上的资料真的不是太多。
尤其是例子，主要都是以 `asyncio.sleep()` 和 `aiohttp` 为主。
其他实际处理同步变成异步的方法，少之又少。
不知道是没有这个需求，还是其他原因。

之前试过 gevent 好像非常方便，就几行代码就把同步变成异步。
asyncio 有点复杂。可能是我对异步、同步、线程、进程、协程...一大堆概念，实在还没能弄个清楚。

现在试图一步一步的学习。

网上例子举得最多的是 `asyncio.sleep()`。 的确很神奇，按照例子做，当然是可以的。

```python
import asyncio

async def get_sleep():
    print('Start {}'.format(n))
    await asyncio.sleep(1)
    print('End {}'.format(n))

tasks = [asyncio.ensure_future(get_sleep(i)) for i in range(1,4)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

Result:
```bash
Start 1  \
Start 2  ----- almost the same time
Start 3  /
End 1  \
End 2  ----- almost the same time
End 3  /
Time: 1.0080575942993164 sec.
```


然后都会跟一句话，“在实际应用中，把`asycio.sleep()`换成实际的IO就可以了。”
这句话，实在没有说清楚。
因为如果把它换成 `requests.get()`就没用了，因为`requests` 是基于同步的。
那就是说，要把`asyncio.sleep()`换成基于异步的IO 才能用例子中这样简单的代码完成。

那基于异步的 IO 又有哪些呢？呃~~ That is the question.






### 参考
* Python 异步协程 Coroutine  [>>](https://quxiaowei.github.io/post/python_async/ 'github.io')
* Python并发编程之协程/异步IO  [>>](https://segmentfault.com/a/1190000007851357 'segmentfault.com')
* 深入理解python3.4中Asyncio库与Node.js的异步IO机制  [>>](http://python.jobbole.com/87431/?utm_source=blog.jobbole.com&utm_medium=relatedPosts 'jobbole.com')
* 用 Python 3 的 async / await 做异步编程  [>>](http://python.jobbole.com/88427/ 'jobbole.com')
* Python 协程从零开始到放弃  [>>](https://lightless.me/archives/python-coroutine-from-start-to-boom.html, 'lightless.me')
* 理解 Python asyncio [>>](http://lotabout.me/2017/understand-python-asyncio/ 'lotabout.me')
* Python 协程：从 yield/send 到 async/await [>>](http://www.woola.net/detail/2016-10-18-python-coprocessor.html 'woola.net')
* gevent：轻松异步 I/O  [>>](http://python.jobbole.com/84301/ 'jobbole.com')
* 深入理解 Python 异步编程（上）[>>](http://python.jobbole.com/88291/ 'jobbole.com')