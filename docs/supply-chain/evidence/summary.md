# Reproducibility Pilot Summary

- Image: `app-stayhealthy-backend`
- Status: `mismatch`
- Comparison basis: `oci_manifest_digest`
- First manifest digest: `sha256:012c758f27c38927e2899edffb7a881dc89371c8d5a37cece0a422727593150c`
- Second manifest digest: `sha256:de35a4c77689d219eadbd2be97782f38097875b99d73cafbfee7ce0ad31ea555`
- First config digest: `sha256:159ac719dc1d23b9107a47ea0627497cca4efc6d89e3d053a7dd82084177eca5`
- Second config digest: `sha256:04ef9c4200aa575542b3c5e0bd188a5323526434420d125257b290e8ab4ec323`
- First layer count: `9`
- Second layer count: `9`
- First platform: `linux/amd64`
- Second platform: `linux/amd64`

Detailed comparison:
- Config digest match: `False`
- Layer count match: `True`
- Layer digests match: `False`
- Layer digest differences: `3`
- Config JSON field differences: `3`

Layer digest differences:
- Layer `5`: first `sha256:311d2326a5fa9c598d72fb7ee96417199bf47ee8b5454436e59212e44a186a9d`, second `sha256:fab3d8ab751d3696d4085e9ad23af17078a4505536a261e66cd27fcfa9115a40`
- Layer `6`: first `sha256:53a7139130e3c513fa9a8226782735ee2889fef95b7a17d434bd13a37900642b`, second `sha256:c9b198057eb9127c1450213ffce03190104f4e8adf3d398a63fe9ff773665644`
- Layer `7`: first `sha256:243590b85f95260b6ea6862c531f4da0ce6afd5d702875e84f011fe2e59b0e72`, second `sha256:7ab648950e4b33586d67c416e95e9010a65b38e4b7fe7423b578087cbac931e8`

Config JSON field differences:
- `rootfs.diff_ids[5]`: first `sha256:1e9bdcc78e411498115ff284b206caf0a6f0b7a31cbf46c34df9eda10a3952a5`, second `sha256:200fc841a41499e7c780dc55da1a925f206e176bf971f1182d6b192609127765`
- `rootfs.diff_ids[6]`: first `sha256:f77b6f88c60c36e4b8f0f5bd3e4d30da045664612cdde993b4eec32bc0911f4c`, second `sha256:e84bf2325827da1532f04e65714a6bd7016952ddb4944191902a586b9c389e7f`
- `rootfs.diff_ids[7]`: first `sha256:9cbe9294db66297e186eab9f10c3b4084716d416f9b0c4e31ebeb164610331be`, second `sha256:95eb64db567a35e7e02a3a01f0af9bfa2d34d881b0a43b3c26379b7dfc5865d7`

Interpretation:
- The two normalized OCI builds produced different manifest digests. Treat this as a reproducibility pilot failure that needs investigation before using the result as evidence.

Artifacts:
- `report.json`
- `summary.md`
