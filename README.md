simplejsdoc
===========

Simple Python tool to extract JSDoc from Closure-style codebases and prepare a API reference in HTML.

Background
---

The [existing Closure API docs](http://closure-library.googlecode.com/svn/docs/index.html) were released around the time the Closure Tools suite was open sourced. It's a system very tied up with
[Grok](https://news.ycombinator.com/item?id=4371267), which is great, but is largely proprietary and cannot be open sourced.

There had been some effort to repurpose [Closure Linter](http://closure-linter.googlecode.com)'s [parsers and tokenizers](https://code.google.com/p/closure-linter/source/browse/trunk/closure_linter/javascripttokenizer.py) to do this job, but it turned out somewhat more difficult than expected to reuse that code, and the effort stalled and was eventually abandoned.

Other JsDoc systems _kind of_ work on Closure, but the flag/type syntax used by Closure is foreign to these tools.

I, [nanaze](http://github.com/nanaze), wanted to take a shot at doing this in a more lo-fi manner, possibly repurposing an exisiting parser like [Esprima](http://esprima.org/). But quick prototyping led me to extract JsDoc with regular
expressions in Python which, though duct-tape-like, works surprisingly well and quickly.
