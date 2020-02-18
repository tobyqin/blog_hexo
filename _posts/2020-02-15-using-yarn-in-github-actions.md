---
title: 在Github Actions中使用Yarn
categories: [Tech]
tags: [github,nodejs,yarn,npm]
date: 2020-02-15
---
Yarn的呼声时不时比npm大，在Github Actions里怎么使用Yarn呢？

<!-- more -->

## 用 npm 的示例

```yaml
name: Node CI

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [8.x, 10.x, 12.x]

    steps:
    - uses: actions/checkout@v1
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v1
      with:
        node-version: ${{ matrix.node-version }}
    - name: npm install, build, and test
      run: |
        npm install
        npm run build --if-present
        npm test
```

## 通过npm来安装Yarn

```yaml
...
steps:
- uses: actions/checkout@v1
- name: Uses Node.js ${{ matrix.node-version }}
  uses: actions/setup-node@v1
  with:
  	node-version: ${{ matrix.node-version }}
- run: npm install -g yarn # Extra Step
...
```

## 用Yarn替换掉npm

```yaml
...
- name: yarn install, build, and test
  run: |
    yarn install
    yarn run build
    yarn test
```

##  完整的例子

```yaml
# .github/workflows/nodejs.yml
name: Node CI

on: [push, pull_request] # Run on Push and Pull Requests

jobs:
  build:

    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [10.x] # Only run the 10.x build

    steps:
    - uses: actions/checkout@v1
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v1
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm install -g yarn
    - name: yarn install, build, and test
      run: |
        yarn
        yarn build
        yarn test
```
