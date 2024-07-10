# Template Project

> How to initialize a new project: [INIT.md](./INIT.md)


**Application Code**

Application entry points.

Path: [apps/application](apps/application/README.md)

**Application Deployment**
Infrastructure as Code for the application

Path: [apps/deployment](apps/deployment/README.md)

**Application System Tests**

Run tests against a deployed (non-productive) environment.

Path: [apps/system-tests](apps/system-tests/README.md)


**BitBucket Pipelines Permissions**

Setup BitBucket pipelines permission in AWS via Infrastructure as Code.

Path: [apps/bitbucket-pipelines](apps/bitbucket-pipelines/README.md)

## Setup

**node**

Install the Node version defined in the [`.nvmrc`](.nvmrc) file at the root of the repository.
It is recommended to use [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) for this:

1. see [GitHub page](https://github.com/nvm-sh/nvm#installing-and-updating) or [this instructions for windows](https://dev.to/skaytech/how-to-install-node-version-manager-nvm-for-windows-10-4nbi)
2. run `nvm install` in the root of this repository (installs version which is pinned in [`.nvmrc`](.nvmrc))
3. you can run `nvm use` in the root of the repository to switch to this node version
4. (optional) add nvm config (see [nvm config](./docs/nvm.md))

## Working with this repository

### Structure

```
./apps
./docs
./libs (if needed)
./tools
```

**apps**

Application code which can be run locally or in an deployed environment.

The template starts with one package for application code (`application`) and one package for the deployment (`deployment`).
If you have reason to, you may split the application and/or deployment package into multiple packages.

See that system tests are `system-tests` is placed into a separated package to

- avoid mixing test logic and application logic
- be able to reference logic from the deployment (system test config)

The package `bitbucket-pipelines` helps to setup OpenID Connect roles for best practices deployment via Bitbucket Pipelines.

```
apps
|--- application
|--- bitbucket-pipelines
|--- deployment
|--- system-tests
```

**docs**
Repository wide documentation shall be placed here and referenced where needed.

**libs**

Libraries which can be used by other libraries and application packages.

**tools**

Build, test and deployment tooling which can be used by multiple packages or a deployment pipeline.

### Install dependencies

When you have node version defined in [`.nvmrc`](.nvmrc) up and running, run

```sh
npm run install-dependencies
```

in the root of the repository.

### Commands

Common commands are:

- **codegen** - perform code generation steps
- **format** - perform formatting
- **lint-fix** - perform linting and apply auto-fixable fixes
- **type-check** - perform type checking
- **test** - perform unit testing

**Run commands**

This repository uses the [npm workspace](https://docs.npmjs.com/cli/v7/using-npm/workspaces) feature, to connect the node packages maintained in here.
By separating code into packages, we can more easily enforce module boundaries.

On top of that, we use [Nx](https://nx.dev/getting-started/intro) as mono repo manage which builds on top of the npm workspace feature.
The task of Nx is not to connect the packages, but to coordinate the execution of tasks we want to perform.
Moreover, Nx can be used independently of the used programming language which helps to maintain for instance some Python or Go Lambdas functions in a mainly TypScript powered codebase.

Using Nx is optional.
You can still run node scripts as if Nx is not there.
Here are examples for the `test` script:

```sh
# executed in the root of the repository;
# sequentially runs the script test of each package in the workspace when the package defines that script
npm run test --workspaces --if-present

# when you are in the directory of a package, you can still run scripts as if there is no npm workspace setup
npm run test
```

Among many other features, Nx allows you to define the dependencies between tasks in the [`nx.json`](nx.json) file.
When you run a task via Nx, a dependency tree is calculated and it is ensured that when task A depends on task B, task A is not performed before task B.
On the other hand, Nx can run tasks in parallel which do not conflict.
Here are examples of running the `test` task:

```sh
# runs the test task of each package in the workspace and all tasks which this task depend on
npx nx run-many -t test

# runs the test task of the package named "package-name" and all tasks which this task depend on
npx nx run package-name:test

# runs the test tasks of each package in the workspace and all tasks which this task depend on (but each one only once)
npx nx run-many -t test type-check build
```

When you want that type checking is always performed before lint-fix and codegen alters the code of a package, you can define this in the [`nx.json`](nx.json) file like this:

```json
"type-check": {
   "dependsOn": ["lint-fix", "codegen"]
}
```

You can use `^` to tell Nx that the specified task after `^` has to be executed for all dependencies of this package first.
This is common, for instance, for build task, when a package wants to consume the output of the build of another package.

```json
"build": {
   "dependsOn": ["^build"]
}
```

> With `npx nx graph`, you can visually explore the dependencies between your packages.

See [Nx features](https://nx.dev/features) for a more in depth explaination.

### Branching

TODO:

- when I want to create a new feature, where do I branch off?
- against which branch do I create pull requests for that feature
- which changes are released, when and how?

> Note: you can edit this branching model image with the drawio plugin for VSCode and IntelliJ

![branching-model](./docs/workflows/branching-model.drawio.svg)

### Update and sync dependencies of packages

If you want to update dependencies, you can use [synpack](https://jamiemason.github.io/syncpack/).

```sh
npx syncpack update # interactively update packages (you can select what dependencies to update or which to skip)

npx syncpack fix-mismatches # assert that all packages are in sync
```

Take a look at the synpack documentation as well as the [.syncpackrc.cjs](.syncpackrc.cjs). The typescript version, for instance, is pinned there so it does not offer an update every time.

There may be cases and projects where you don't want every package to use the same version of the same dependency.
This works fine too, since npm-workspaces then creates a `node_modules` folder into the packages with those dependencies which conflict by their version with others in the repository.

Tip: If you want to delete all `node_modules` folders in you repository, you can use:

```sh
find . -type d -name "node_modules" -exec rm -rf {} \;
```

Sometimes, deleting all `node_modules` folders and the `package-lock.json` can solve clean-install dependency problems.

## Architecture of applications

The architecture of the run time code should the [Hexagonal Architecture](<https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)>) in mind.
It builds on top of the three-tier-architecture but describes everything from the point of view of the domain and application.

In the center of everything is the domain and the problem we want to solve.
The domain itself has no notion of databases and webserver endpoints.
It encapsulates the business rules in **Domain Services** and models its data in **Domain Entities**, which are shown in the center of the architecture diagram below.

**Use cases** can use Domain Services and **Accessors** in order to model processes.
Those can be reused and don't know by which event they were invoked.

**Accessors** provide the abstraction to handle the persistence of domain entities
or map those for the interaction with other systems or service endpoints.
The interaction with databases or other systems are done by **DataClients**.
Under the hood, Accessors use a _persistence model_ which represents the data used by the persistence service or external system.
Accessors should be abstracted via interfaces to increase the modularity of the application.

**DataClients** provide the basic capabilities to communicate with another system or service endpoint.
They do not have knowledge about the domain.
DataClients can be abstracted via interfaces to increase the modularity of the application.

**Controllers** parse and/or validate the invocation request, delegate them to UseCases or Accessors and format the response for the callee.
They do not perform low-level database or low-level service request.

![architecture-idea](./docs/architecture/hex-architecture-idea.drawio.svg)

## Deployment

**Pipeline**

- [bitbucket-pipelines.yml](./bitbucket-pipelines.yml)
- [bitbucket-pipelines package](./apps/bitbucket-pipelines/README.md)

**Application Deployment**

- [Application Deployment](./apps/deployment/README.md)
