# Reproducibility Pilot Summary

- Image: `app-stayhealthy-backend`
- Status: `mismatch`
- Comparison basis: `oci_manifest_digest`
- First manifest digest: `sha256:ba392bdf0162f2d214ac3a394eb71d1828725566f2bd579a1e27d4d34c5b8b7e`
- Second manifest digest: `sha256:bac4cd95aa3370a295a3691d1094f3770b7241844daf51bd88c5f9fb6e02e278`
- First config digest: `sha256:d7e99fcfba5357ccf3a02a4b56b72955472ad1e31de35f068a8b6b428f50a6f8`
- Second config digest: `sha256:af4344654092f8d3123ef6ebb2da0dc61d8693b9d7b9e46874dd1705a9a9d891`
- First layer count: `9`
- Second layer count: `9`
- First platform: `linux/amd64`
- Second platform: `linux/amd64`

Detailed comparison:
- Config digest match: `False`
- Layer count match: `True`
- Layer digests match: `False`
- Layer digest differences: `3`
- Config JSON field differences: `14`

Layer digest differences:
- Layer `5`: first `sha256:1b295c82257cfb94c95a94bb6247ec813be21aa5e0901136b4ad22f73ab5a1d0`, second `sha256:d1068aefc3966a23c873276813e71e654cd0e7ace2ea4e0a4f276a9bfa51d265`
- Layer `6`: first `sha256:b4f5adbd58d0060a2e7ec7046dd152dcb46a9ff42d58fe396ca315e6812e70d7`, second `sha256:3d943b498461c8b4330720bad4a88f259d79d8275c0dd7196a4e97391831ef44`
- Layer `7`: first `sha256:9edc47630f38e2bbfbd45285617f152a0c94d48e4f5d657ad6504242ee64019e`, second `sha256:d9393aa51169dbcd4f93039ae10af7cc82c21dcd1e5dffa6229a63dd768c30a0`

Config JSON field differences:
- `created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `history[15].created`: first `2026-05-08T18:03:23.324005971Z`, second `2026-05-08T18:03:30.054239663Z`
- `history[16].created`: first `2026-05-08T18:03:26.120845019Z`, second `2026-05-08T18:03:32.869226812Z`
- `history[17].created`: first `2026-05-08T18:03:26.120845019Z`, second `2026-05-08T18:03:32.869226812Z`
- `history[18].created`: first `2026-05-08T18:03:27.477638411Z`, second `2026-05-08T18:03:34.35290093Z`
- `history[19].created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `history[20].created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `history[21].created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `history[22].created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `history[23].created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `history[24].created`: first `2026-05-08T18:03:27.564138489Z`, second `2026-05-08T18:03:34.436273103Z`
- `rootfs.diff_ids[5]`: first `sha256:2a161917c2bca7db5e59485d974280c9ce37b5236eea08f9b62b3688230a6946`, second `sha256:400fd4838f0eb1f6057e1e12d3b3429b2a48b46ec9e60973b9d86552b85eb69b`
- `rootfs.diff_ids[6]`: first `sha256:3de642fc46023b67b6702d13c40e2a7e9af40816554744f3172773e1d6ec1ff7`, second `sha256:e996ce6712252fcf79df6d0e07c777910946942e7f726205a11c35d7340f7c27`
- `rootfs.diff_ids[7]`: first `sha256:54dbe142da837b4f7c38d7e82c8751d5265b29c064dc993a50a2f9aff735661a`, second `sha256:2a28f798eedee972e145d51027fd66a55b32b5eb8471fce640b84f4528b1e17c`

Interpretation:
- The two normalized OCI builds produced different manifest digests. Treat this as a reproducibility pilot failure that needs investigation before using the result as evidence.

Artifacts:
- `report.json`
- `summary.md`
