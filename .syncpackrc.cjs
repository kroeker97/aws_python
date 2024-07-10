// @ts-check

/** @type {import('syncpack').RcFile} */
const config = {
  // formatting done by other tools
  formatRepository: false,
  // sorting done by other tools
  sortPackages: false,
  lintFormatting: false,
  versionGroups: [
    {
      label: 'Node Types',
      dependencies: ['@types/node'],
      pinVersion: 'ts5.5',
    },
    {
      label: 'TypeScript',
      dependencies: ['typescript'],
      pinVersion: '~5.5.2',
    },
    {
      label: 'AWS SDK v3 clients',
      dependencies: ['@aws-sdk/client-**'],
    },
    {
      label: 'CDK',
      dependencies: ['aws-cdk', 'aws-cdk-lib'],
    },
    {
      label: 'CDK Alpha',
      dependencies: ['@aws-cdk/*'],
    },
    {
      label: '@types packages should only be under devDependencies',
      dependencies: ['@types/**'],
      dependencyTypes: ['!dev'],
      isBanned: true,
    },
    {
      label: 'ts',
      dependencies: ['@tecracer/*'],
      dependencyTypes: ['dev'],
      policy: 'sameRange'
    },
    {
      label: 'Use workspace protocol when developing local packages',
      dependencies: ['@template/*'],
      dependencyTypes: ['dev'],
      pinVersion: '*',
    },
  ],
  semverGroups: [
    {
      label: 'Dependencies with tags instead of semver ranges',
      dependencies: ['@types/node'],
      packages: ['**'],
      isIgnored: true,
    },
    {
      label: 'Use exact versions for dependencies by default',
      packages: ['**'],
      dependencies: ['**'],
      range: '~',
    },
  ],
};

module.exports = config;
