# Bootstrapping

To create your own `bomard.yaml` use the command `--init`.
By default, it copies the example `easy.yaml`

```bash
bombard --init
```

Now the `bombard` command will use this local `bomard.yaml`.
Edit it to adapt to your server.

If you want to use another example as base, just add `--example <name>`
with the example name you want:

```bash
bombard --init --example simple
```

To list all available examples, use `--examples` like this:

```bash
bombard --examples
```
