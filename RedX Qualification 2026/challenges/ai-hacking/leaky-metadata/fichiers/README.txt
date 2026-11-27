Leaky Metadata
==============

During an internal audit, our ML team exported a small classifier that
approves or denies access requests. It was supposed to ship with nothing but
weights. The CI pipeline then "sealed" a release token next to it.

Your job: recover the sealed token from flag.enc.

Files
-----
  model.pt   exported checkpoint (PyTorch format)
  flag.enc   sealed release token(s), one per line

Notes
-----
  * Everything you need is inside these files. No network, GPU or PyTorch
    install is required (Python 3 + the `cryptography` package is enough).
  * Never torch.load() a checkpoint you do not trust - pickle can run code.
    Inspect first; if you do load it, use weights_only=True.
  * Not every key you find is the right key.

Flag format: RxR{...}
