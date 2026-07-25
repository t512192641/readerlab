# T2.26 v03 material selection manifest

Frozen before reading the selected member's raw bytes.

- source: `materials/T2.4-IDEA-PILOT-01/source.epub`
- source SHA-256: `3baf9932c92412f0e7d0ccae993182f55f62e2fab5ec46a3882d675476288664`
- excluded chapters: `7, 13, 14, 15, 16, 19`
- eligible count: `15`
- payload bytes: `250`
- payload SHA-256: `16b480aa130a24d8fa1e3e925fb0eaa32740c732271691afd3cf87bdb27e70c3`
- selected zero-based index: `1`
- selected ID: `eligible-02`
- selected chapter: `2`
- selected member: `text/part0006.html`
- selected member bytes: `82261`
- selected member SHA-256: `ba0c9aa2a7413d6792cf1b57b821dc38bd3d6777d5a16cb0dcd69c4dd9442e82`

## Independent algorithm runs

Both runs used only the frozen source SHA-256, `toc.ncx`, ZIP member names/sizes/binary SHA-256, and the frozen exclusions. Their eligible mapping, payload, index, selected ID, chapter, member, size, and SHA-256 were identical.

| eligible ID | chapter | member | bytes | member SHA-256 |
| --- | ---: | --- | ---: | --- |
| eligible-01 | 1 | `text/part0005.html` | 40736 | `6afd6a4ad39ae918ecaffd3207062b0add12c79226b25e6c77a6b1203f6d54b9` |
| eligible-02 | 2 | `text/part0006.html` | 82261 | `ba0c9aa2a7413d6792cf1b57b821dc38bd3d6777d5a16cb0dcd69c4dd9442e82` |
| eligible-03 | 3 | `text/part0007.html` | 85472 | `50fd3d8a1efca1ad48781d4ee953f88d1326fc7c1a99627945c127cfbdc644e5` |
| eligible-04 | 4 | `text/part0008.html` | 21298 | `aa624de483a224ea96d2b00644727910848f38a9d818f18f8949d9eed143b8e2` |
| eligible-05 | 5 | `text/part0010.html` | 17493 | `2ed0019625b947fb46b4d8516552175d97e905aff132f7c81d07e151dd80a3d3` |
| eligible-06 | 6 | `text/part0011.html` | 62852 | `2216583f434c12905c624c407a4c832676e8f7c50d360f885746d9845b615761` |
| eligible-07 | 8 | `text/part0013.html` | 34513 | `e46e57832afe5e89130a8884613ed62c0febc14e87c6cc59485328be7ba95bc8` |
| eligible-08 | 9 | `text/part0014.html` | 43574 | `74ae37f2e1bbc6f49b561e6640fd3d90f21c1cd5e9d2971608459733935c5b72` |
| eligible-09 | 10 | `text/part0016.html` | 33271 | `651c76a45d15e2c9a733675caf29e194e3b770ee1ffabd1da5253ef1dc4efe36` |
| eligible-10 | 11 | `text/part0017.html` | 37956 | `c0eeb4e8be0ae770efd6b2e1d5647d94ed5e4a1c08d8709b80a4e6987deb33e9` |
| eligible-11 | 12 | `text/part0018.html` | 67985 | `dda0e54fdab1045c7b35f6b0754222db21ba1195570caa0eb929cb03faaf7e2d` |
| eligible-12 | 17 | `text/part0024.html` | 48337 | `d97caca7d0650be4cc6f6e36a680a7a7c64fa6ff4e45e2eb0ef013ba25e9db5d` |
| eligible-13 | 18 | `text/part0025.html` | 29817 | `f49d547e7bed12fd2b897b2a9e839225a429603dc8df9d0687a63b6b97379010` |
| eligible-14 | 20 | `text/part0028.html` | 128850 | `3b4663e249f5f9d237a3d3a5dad8f7fed40293c122b9fca105023061b39704fb` |
| eligible-15 | 21 | `text/part0029.html` | 19251 | `dff35dc4e30a9db0069f48dabab2d233185489c0175588e4be6bb5b26acb9982` |

Run 1 and run 2: `IDENTICAL`.
