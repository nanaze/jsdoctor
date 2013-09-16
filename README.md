jsdoctor
===========

Simple Python tool to extract Closure-style [JSDoc](http://en.wikipedia.org/wiki/JSDoc) from Closure-style codebases and prepare a API reference in HTML.

Background
---

The [existing Closure API docs](http://closure-library.googlecode.com/svn/docs/index.html) were released around the time the Closure Tools suite was open sourced. It's a system very tied up with
[Grok](https://news.ycombinator.com/item?id=4371267), which is great, but is largely proprietary and cannot be open sourced.

There had been some effort to repurpose [Closure Linter](http://closure-linter.googlecode.com)'s [parsers and tokenizers](https://code.google.com/p/closure-linter/source/browse/trunk/closure_linter/javascripttokenizer.py) to do this job, but it turned out somewhat more difficult than expected to reuse that code, and the effort stalled and was eventually abandoned.

Other JsDoc systems _kind of_ work on Closure, but the flag/type syntax used by Closure is foreign to these tools.

I, [nanaze](http://github.com/nanaze), wanted to take a shot at doing this in a more lo-fi manner, possibly repurposing an exisiting parser like [Esprima](http://esprima.org/). But quick prototyping led me to extract JsDoc with regular
expressions in Python which, though duct-tape-like, works surprisingly well and quickly. <em>Update: I have begun migrating over to esprima and pulling symbol/JSDoc info from the resulting AST. This work is in esprima.py, genfiletree.py, processfiletree.py</em> 

Design Goals and Guidlines
---

These are explicit decisions made to keep the codebase small and simple:

  * Support Closure-style JSDoc. And that's it -- no generalization for different JSDoc dialects for the sake
  * Fail fast with errors, not warnings -- if parser or doc generator sees a problem, it pukes, as there's something
    with your code.  Writing a test to verify that docs build on each checkin/commit is encouraged.

Current state
---

The tool is not done.  Enough is implemented at present to identify all JSDoc'd symbols in the current Closure codebase and extract the
associated JSDoc comments.

Right now, the tool can do mimimal rendering to HTML.  The following needs to be implemented:

* Rendering of functions.
* Inheritance
* "this.foo" properties
* lots more

If you'd like to contribute, let me know by sending an email.
