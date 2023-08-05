# Bloggo

Bloggo is yet another blog-oriented static site generator.

![linter and tests](https://github.com/askonomm/bloggo/workflows/.github/workflows/linter-tests.yml/badge.svg)

## Requirements

- Python 3.9+
- [pip](https://pip.pypa.io/)

## Installation

1. Run `python -m pip install bloggo` to install Bloggo
2. Get [Bloggo's Boilerplate](https://github.com/askonomm/bloggo-boilerplate) for your site's template and content
3. When ready, generate site with `python -m bloggo` in the directory where `resources` are

That's it, your static site should be available in the `public` folder that was just created.
Every time you make changes, run `python -m bloggo` again to generate 
new files. You can upload your `public` folder's contents to any hosting provided you'd like.

## Updating

To update Bloggo to [the latest version](https://pypi.org/project/bloggo/) simply run:

```bash
python -m pip install bloggo --upgrade
```

To find out what version of Bloggo you are currently running, open your shell and run:

```bash
python -m bloggo --version
```

## Content

Content files are very simple, YAML-esque (but one-level only!) structures. A complete example of a content file looks like this:

```yaml
---
title: Hello, World
decription: A post about welcoming oneself to the world
date: 2021-02-12
---

Markdown content follows here.
```

- Dates have to be in a year-month-day format (you can format it later to whatever you want using the `format_date` helper)
- Files have to be in a `.md` extension, such as `hello-world.md` and placed inside the 
`resources/content` directory. What's MD you say? It's [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet). Beautiful, glorious, best friend of an efficient writer.

## URLs

If you have a file called `hello.md` in the root of the `resources/content` directory, then that content
will be available via yoursite.com/hello. Likewise, if you put your stuff in a directory itself, like in a case of a blog post you would 
have a file in `resources/content/blog/hello.md`, then that  content will be available via yoursite.com/blog/hello.

**Note:** the way Bloggo is written is that it always expects blog posts to live in the blog directory. I may 
at one point make it configurable (or you can make a pull request), but for now it is what it is.

## Watch files for changes

In order to ease development of static sites with Bloggo, you can run it with a watcher via the 
`--watch` flag, which will then monitor the `resources` directory for any changes and 
upon detecting a change, generates a new static site.

## Specify directories

By default, Bloggo expects resources to live in the `resources` folder, and the 
generated files will end up in a `public` folder. If you don't like this however, you can
change it by passing a `--resources-dir` and/or `--out-dir` flags when calling Bloggo to change this.

For example:

```bash
python -m bloggo --resources-dir ~/site/resources --out-dir ~/home/public_html
```
## Templating

Bloggo uses Handlebars to put together your static site. It runs in a single templating file, called `template.hbs`, in `resources` directory.
I encourage you to make it your own, change things around and go crazy. But if you won't, that's okay, too.

### Variables

#### Global variables:
- `is_home` returns true when being on the home page of the site
- `is_post` returns true when any content item is being viewed

Additionally, any configuration that you have added to  the `resources/config.json` file will be available as it's own 
variable as well. For example a config such as:

```json
{
  "site_title": "Doggo's Bloggo"
}
```

would be usable in the template as `{{site_title}}`.

#### Contextual variables

Each of the posts yaml-esque key: value configuration is also available to you, in the post's context.
Post context is available in two places:

When you are inside a `is_post` context, you can simply access all the post's variables as-is. An example use-case would be:

```handlebars
{{#if is_post}}
    <h2>{{title}}</h2>
    <div class="date">{{date}}</div>
    <div class="entry">{{entry}}</div>
{{/if}}
```

However, when you are inside a `is_home` context, you c an access all the post's
variables from within a loop. An example use-case would be:

```handlebars
<ul>
    {{#posts}}
        <li>
            <h2>{{title}}</h2>
            <div class="date">{{date}}</div>
            <div class="entry">{{entry}}</div>
        </li>
    {{/posts}}
</ul>
```

You see all the post's yaml-esque key: value things are available as `{{key}}`, and the content of the post is available as `{{{entry}}}`. Note 
the three curly brackets, which Handlebars will render HTML with. 

#### Helpers

##### `format_date` helper

Allows you to format a given `date` into any format you'd like, like this:

```handlebars
{{format_date date "%b %-d, %Y"}}
```

Which would output something like February 14, 2021. For a full list of things
you can pass it to format your date, [refer to this documentation](https://strftime.org/).

### Assets

You should add your images, stylesheets, fonts and so on in the `resources/assets` directory. This will get copied over
to the `public` directory when generating, so your assets will be available via yoursite.com/assets/{...} 