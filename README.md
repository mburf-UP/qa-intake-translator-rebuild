# qa-intake-translator — rebuild

Comp #15 (The Rebuild) entry. Work in progress.

- `original/` is the judged comp #13 entry, exported unchanged with `git archive` from
  [mburf-UP/qa-intake-translator](https://github.com/mburf-UP/qa-intake-translator) at commit
  `ed18d22f7e2d244df57cc762bec4080fafc8314e` (tree `dbc68c319ce37056d2aa58ff1d591a6ea68fbecf`).
  Nothing inside it is added or changed, in this commit or any later one.
- `feedback.md` is the judges' feedback file for that entry, verbatim
  (SHA-256 `ee07ac0bb9a8479c867dab84a39553f20ca2c27b43a1068734e80141aa4995b0`).

To check the pin yourself:

```sh
git clone https://github.com/mburf-UP/qa-intake-translator /tmp/orig
git -C /tmp/orig checkout ed18d22f7e2d244df57cc762bec4080fafc8314e
diff -r --exclude=.git /tmp/orig original && echo "original/ matches ed18d22"
```
