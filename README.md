# Assistant Robotic Musician

> To address the difficulty musicians face when performing without an assistant
  or deskmate, we will create an Assistant Robotic Musician (ARM) which can
  fulfill the same role more efficiently and less intrusively. The ARM will be a
  free, open-source, cross-platform application into which one can load sheets
  of music or e-booklets of sheet music, with embedded software to process live
  audio of the performance and automatically determine when to flip the page.
  Additionally, it will automatically process scanned sheet music, as well as
  allow for editing, storing and organizing these processed files in a vast
  library. Furthermore, the eponymous, friendly AI, “Arm,” will manage both the
  library and the performance software. We hope to make this a collaborative
  effort, inviting musicians to write sheet music compatible with the ARM.
  Together, we hope to ease the process of performing with sheet music by
  removing distractions and difficulties in handling the music.


### About This Repository
This repository contains the online presence of the Assistant Robotic Musician,
an engineering project (specifically, a Senior Capstone Design Project) that
aims to create a product which seamlessly and responsively turns the pages of
the digital sheet music, contained in its library, as a musician performs.

Specifically, this repository contains, or will contain, two separate but
connected projects: The various scripts that make up the software component of
the ARM, and the code that deploys the ARM's webpage:
<https://assistant-robotic-musician.herokuapp.com>.

### Contents
01. [Assistant Robotic Musician](#assistant-robotic-musician)
02. [About This Repository](#about-this-repository)
03. [Contents](#contents)
04. [Scripts](#scripts)
05. [Webpage](#webpage)

### Scripts
All technical scripts and files are stored in the `app` subdirectory of this
repository and should be developed in the `app` branch. There are two parts to
this subdirectory: `main` and `workshop`.

##### `main`
The `main` part of the `app` is composed of `scripts/index.js`, `scripts/HTML/`,
and any relevant NodeJS files (`package.json`, `package-lock.json`, etc.). This
portion represents the functional part of the app: the ElectronJS packaging, the
User Interface, and any connected technical scripts. This portion of the
subdirectory should be seen as the "official" presentation, or the "face" of the
app; of course, it too will undergo development, but it is not experimental in
the way the workshop is.

At the moment, the functional app consists of: a stupidly basic HTML server.

<!--Use this space to add details about development of `main`-->

##### `workshop`
The `workshop` part of the `app` is contained entirely in `scripts/workshop/`.
It is the technical, experimental part of the app. Any new components should
start their development in `workshop`, only graduating to `main` when they have
been thoroughly tested and prepared for implementation.

Every script in `workshop` should contain a block comment explaining the
script's purpose, current knowledge about the experiment, current successes and
problems, and any other relevant information. These scripts include:

01. `01_NodePy`: A Python3 and a NodeJS pair for using Python within the app
    - Demonstrates a variety of functions, from running python one-liners, to
      super basic text-based output from a script, to full-blown input/output
    - Still missing: JSON Output example, (?) continuous stdin/stdout/stderr
    - Numerous examples, each in their own code block, of having the apps
      interact in different ways---primarily, NodeJS feeding data to Python
    - Essential learning: Embedding Python is not difficult at all, we basically
      just need to treat the script as if it's a function that we feed data
02. Other experiments to start:
    - Sheet Music Markup Language (`SMML`) & displaying SMML
    - Python audio processing

<!--Use this space to add details about development of `app`-->

### Webpage
<https://assistant-robotic-musician.herokuapp.com>

##### Development
All code relevant to the website is stored in the `web` subdirectory of this
repository. This subdirectory is also what is known as a `git subtree`, which
is an embedded repository within this repository. For all intents and purposes,
the website can be developed as if it's a regular subdirectory of this
repository; the only complexities are in the [deployment](#deployment), below.

Website development should take place in the `files` branch (named for the
"files" that make up the website). Use `npm test` within the `web` subdirectory
to mimic the Heroku functionality. Whenever a bulk update to the website has
been completed and thoroughly tested---to minimize needless pull requests and
the likelihood of the website crashing---then a pull requset can be created for
that update

##### Deployment
In addition to being version-controlled on GitHub, through the broader package,
the code within the `web` subtree is hosted on Heroku. This is, for the most
part, a simple process, for as long as Heroku has a `Procfile` specifying the
entry point of the application, it can run through git just like GitHub.
However, the `Procfile` and entry point must both be in the base level of the
repository on Heroku. This is why `git subtree` is necessary for the development
and deployment of the website, and to properly deploy the code, one must use
the following:

```
git subtree push --prefix web heroku master
```

This command works as follows. Obviously, `git subtree`, invokes the subtree
manager, and `push` tells it to push the code it is fed. We must, however,
specify a `--prefix` of `web` (the subtree we want to push), before we can
specify the remote (`heroku`) and the branch (`master`).
