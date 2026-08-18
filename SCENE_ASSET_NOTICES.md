# Scene Asset Notices

This document contains the license notices, attribution statements, source
references, and modification disclosures for third-party scene assets used by
VisibilityBufferInfo.

The original scene archives are not part of this Git repository. Local scene
copies under `assets/scenes/` are ignored by Git. Benchmark specifications,
numeric results, plots, and validation images may nevertheless identify or
depict these scenes, so their provenance is recorded here.

This document does not license the VisibilityBufferInfo source code and does
not relicense any third-party asset. Each asset remains subject to the license
or EULA supplied by its copyright holder or distributor. Any `LICENSE`,
`LICENSE.txt`, `COPYING`, `README`, credit file, or EULA included with an
original download must be retained with that asset. If a bundled license or
EULA conflicts with this document, the bundled license or EULA governs that
copy.

## Covered assets

| Scene asset | Provider / creator | License |
|---|---|---|
| Bistro Exterior | Amazon Lumberyard / NVIDIA Open Research Content Archive | Creative Commons Attribution 4.0 International |
| Bistro Interior with Wine | Amazon Lumberyard / NVIDIA Open Research Content Archive | Creative Commons Attribution 4.0 International |
| Sponza Atrium 2.0 Base Scene (`Intel Sponza Base Scene`) | Frank Meinl; distributed through Intel GPU Research Samples | See Section 3: Intel distribution notice and ASWF Digital Assets License v1.1 |
| Sponza Atrium 2.0 Ivy add-on | Frank Meinl and the Sponza add-on contributors; distributed through Intel GPU Research Samples | Retain the license/EULA supplied in the downloaded add-on; Intel lists its sample downloads under Creative Commons Attribution |
| San Miguel 2.0 | Guillermo M. Leal Llaguno; archive conversion by Morgan McGuire and contributors | Creative Commons Attribution 3.0 Unported |
| UE4 Sun Temple | Epic Games; NVIDIA ORCA conversion by Kai-Hwa Yao and Nicholas Hull | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International |
| Pawn Shop | Poly Haven and contributing artists | CC0 1.0 Universal |
| The Hidden Alley | Poly Haven and contributing artists | CC0 1.0 Universal |
| The Shed | Poly Haven and contributing artists | CC0 1.0 Universal |
| A Verdant Trail | Poly Haven and contributing artists | CC0 1.0 Universal |
| Namaqualand | Poly Haven and contributing artists | CC0 1.0 Universal |
| Pine Forest | Poly Haven and contributing artists | CC0 1.0 Universal |
| Zero-Day — Measure One | Mike Winkelmann / NVIDIA Open Research Content Archive | Creative Commons Attribution 4.0 International |
| Zero-Day — Measure Seven | Mike Winkelmann / NVIDIA Open Research Content Archive | Creative Commons Attribution 4.0 International |
| Lunar Landscape | Poly Haven and contributing artists | CC0 1.0 Universal |

## Modification disclosure

Unless retained byte-for-byte from an official archive, scene copies used by
VisibilityBufferInfo may differ from the original assets. Modifications may
include:

- archive extraction and directory reorganization;
- conversion between FBX, OBJ, glTF, Blender, or another supported source
  format;
- coordinate-system conversion;
- mesh triangulation;
- generation or recalculation of normals and tangents;
- preservation, realization, or restructuring of instances;
- texture path normalization;
- texture resizing, mip generation, or transcoding;
- simplification or remapping of materials;
- omission of unsupported lights, cameras, animation, procedural nodes,
  displacement, transmission, or other renderer-specific features; and
- addition of benchmark metadata, camera paths, manifests, or cache files.

No third-party creator, provider, or contributor endorses VisibilityBufferInfo,
its benchmark results, or any product tested with these assets.

---

## 1. Amazon Lumberyard Bistro

### Covered scenes

- Bistro Exterior
- Bistro Interior with Wine

### Attribution

> “Amazon Lumberyard Bistro, Open Research Content Archive (ORCA)” by
> Amazon Lumberyard, July 2017. Licensed under the Creative Commons
> Attribution 4.0 International License. Modified for use in the
> VisibilityBufferInfo benchmark as described in the Modification disclosure
> section of this document.

### Source

- https://developer.nvidia.com/orca/amazon-lumberyard-bistro

### License

- Creative Commons Attribution 4.0 International (`CC-BY-4.0`)
- https://creativecommons.org/licenses/by/4.0/legalcode

### Reference citation

```bibtex
@misc{ORCAAmazonBistro,
  title  = {Amazon Lumberyard Bistro, Open Research Content Archive (ORCA)},
  author = {Amazon Lumberyard},
  year   = {2017},
  month  = {July},
  url    = {https://developer.nvidia.com/orca/amazon-lumberyard-bistro}
}
```

---

## 2. Zero-Day

### Covered scenes

- Zero-Day — Measure One
- Zero-Day — Measure Seven

### Attribution

> “Zero-Day, Open Research Content Archive (ORCA)” by Mike Winkelmann,
> November 2019. Licensed under the Creative Commons Attribution 4.0
> International License. The real-time-compatible asset package was converted
> from the original Octane and Cinema 4D formats by Kai-Hwa Yao and Kate
> Anderson. Modified for use in the VisibilityBufferInfo benchmark as
> described in the Modification disclosure section of this document.

### Source

- https://developer.nvidia.com/orca/beeple-zero-day

### License

- Creative Commons Attribution 4.0 International (`CC-BY-4.0`)
- https://creativecommons.org/licenses/by/4.0/legalcode

### Reference citation

```bibtex
@misc{ZeroDay,
  title  = {Zero-Day, Open Research Content Archive (ORCA)},
  author = {Mike Winkelmann},
  year   = {2019},
  month  = {November},
  url    = {https://developer.nvidia.com/orca/beeple-zero-day}
}
```

---

## 3. Sponza Atrium 2.0 Base Scene

### Covered scene

- Sponza Atrium 2.0 Base Scene, distributed by Intel under the title
  `Sponza Base Scene`
- Sponza Atrium 2.0 Ivy add-on, distributed by Intel under the title `Ivy`

### Sources

- Intel GPU Research Samples:
  https://www.intel.com/content/www/us/en/developer/topic-technology/graphics-research/samples.html
- Intel Sponza Base Scene record:
  https://www.intel.com/content/www/us/en/content-details/830833/sponza-base-scene.html
- Creator distribution and EULA:
  https://www.artstation.com/marketplace/p/wbXgz/sponza-atrium-2-0
- ASWF Digital Assets License v1.1 reference:
  https://spdx.org/licenses/ASWF-Digital-Assets-1.1.html

Intel identifies the sample as available under a Creative Commons Attribution
license. The creator distribution supplies the ASWF Digital Assets License
v1.1 for education, training, research, software and hardware development,
performance benchmarking, reproducibility, and product demonstrations. The
copyright notice and ASWF terms are reproduced below. The license or EULA
included in the downloaded archive must also be retained and governs that
copy if its terms differ.

### Copyright notice

> Sponza Atrium 2.0 Copyright 2022 Frank Meinl. All rights reserved.

Publications, figures, slides, videos, and web pages showing images rendered
from this asset must include the copyright notice above when the asset is used
under the ASWF Digital Assets License v1.1.

### Attribution and modification notice

> “Sponza Atrium 2.0” by Frank Meinl, distributed as the Intel GPU Research
> “Sponza Base Scene.” Sponza Atrium 2.0 Copyright 2022 Frank Meinl. Used for
> rendering research and performance benchmarking. Modified copies may differ
> from the original as described in the Modification disclosure section of
> this document.

### ASWF Digital Assets License v1.1

License for Sponza Atrium 2.0 (the "Asset Name").

Sponza Atrium 2.0 Copyright 2022 Frank Meinl. All rights reserved.

Redistribution and use of these digital assets, with or without modification,
solely for education, training, research, software and hardware development,
performance benchmarking (including publication of benchmark results and
permitting reproducibility of the benchmark results by third parties), or
software and hardware product demonstrations, are permitted provided that the
following conditions are met:

1. Redistributions of these digital assets or any part of them must include
   the above copyright notice, this list of conditions and the disclaimer
   below, and if applicable, a description of how the redistributed versions
   of the digital assets differ from the originals.

2. Publications showing images derived from these digital assets must include
   the above copyright notice.

3. The names of copyright holder or the names of its contributors may NOT be
   used to promote or to imply endorsement, sponsorship, or affiliation with
   products developed or tested utilizing these digital assets or benchmarking
   results obtained from these digital assets, without prior written
   permission from copyright holder.

4. The assets and their output may only be referred to as the Asset Name
   listed above, and your use of the Asset Name shall be solely to identify
   the digital assets. Other than as expressly permitted by this License, you
   may NOT use any trade names, trademarks, service marks, or product names of
   the copyright holder for any purpose.

DISCLAIMER: THESE DIGITAL ASSETS ARE PROVIDED BY THE COPYRIGHT HOLDER "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE,
ARE DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THESE DIGITAL
ASSETS, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The ASWF license above is purpose-limited. It permits only the education,
training, research, development, benchmarking, reproducibility, and product
demonstration uses stated in the license. It does not independently grant
unrestricted use for unrelated commercial artwork, entertainment, or asset
resale.

---

## 4. San Miguel 2.0

### Covered scene

- `San_Miguel/san-miguel.obj`, referenced by retained multi-scene benchmark
  specifications and results

### Attribution

> “San Miguel 2.0” was originally modeled by Guillermo M. Leal Llaguno of
> Evolucien Visual. The 2017 research versions were improved by Morgan
> McGuire, Guedis Cardenas, Michael Mara, and Nicholas Hull with permission
> from Guillermo M. Leal Llaguno. The version used by VisibilityBufferInfo may
> contain further benchmark-oriented changes described in the Modification
> disclosure section of this document.

### Source and citation

- Morgan McGuire Computer Graphics Archive:
  https://casual-effects.com/g3d/data10/index.html
- Requested archive citation: Morgan McGuire, *Computer Graphics Archive*,
  July 2017, https://casual-effects.com/data

### License

- Creative Commons Attribution 3.0 Unported (`CC-BY-3.0`)
- https://creativecommons.org/licenses/by/3.0/legalcode

Attribution must identify the original creator and the archive contributors,
link the license, and indicate modifications. The license notice supplied in
the downloaded archive remains authoritative for that copy.

---

## 5. UE4 Sun Temple

### Covered scene

- `SunTemple_v4/SunTemple.fbx`, referenced by retained multi-scene benchmark
  specifications and results

### Attribution

> “Unreal Engine Sun Temple, Open Research Content Archive (ORCA)” by Epic
> Games, October 2017. Exported from Unreal Engine by Kai-Hwa Yao and Nicholas
> Hull. Licensed under Creative Commons Attribution-NonCommercial-ShareAlike
> 4.0 International. The version used by VisibilityBufferInfo may contain
> further benchmark-oriented changes described in the Modification disclosure
> section of this document.

### Source

- https://developer.nvidia.com/ue4-sun-temple

### License

- Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
  (`CC-BY-NC-SA-4.0`)
- https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

This asset cannot be redistributed or used for commercial purposes under this
license. Adapted material must be shared under the same license, with
attribution, a license link, and a change notice. Do not include the scene in a
commercial release without obtaining separate permission.

### Reference citation

```bibtex
@misc{OrcaUE4SunTemple,
  title  = {Unreal Engine Sun Temple, Open Research Content Archive (ORCA)},
  author = {Epic Games},
  year   = {2017},
  month  = {October},
  url    = {https://developer.nvidia.com/ue4-sun-temple}
}
```

---

## 6. Poly Haven scene files

### Covered scenes

- Pawn Shop
- The Hidden Alley
- The Shed
- A Verdant Trail
- Namaqualand
- Pine Forest
- Lunar Landscape

### Provider and creators

Poly Haven and the contributing artists identified on the corresponding
Poly Haven project and asset pages.

### License

- Creative Commons CC0 1.0 Universal (`CC0-1.0`)
- https://creativecommons.org/publicdomain/zero/1.0/legalcode
- Poly Haven license policy: https://polyhaven.com/license

Poly Haven releases its downloadable assets under CC0. CC0 permits use,
modification, and redistribution, including commercial use, without mandatory
attribution. The following voluntary credit is retained for provenance:

> Poly Haven and contributing artists. Released under CC0 1.0 Universal.
> Modified for use in the VisibilityBufferInfo benchmark where applicable.

### Scene pages

- Pawn Shop:
  https://blog.polyhaven.com/pawn-shop-scene-file/
- The Hidden Alley:
  https://polyhaven.com/collections/hidden_alley
- The Shed:
  https://polyhaven.com/collections/the_shed
- A Verdant Trail:
  https://polyhaven.com/collections/verdant_trail
- Namaqualand:
  https://polyhaven.com/collections/namaqualand
- Pine Forest:
  https://polyhaven.com/collections/pine_forest
- Lunar Landscape:
  https://polyhaven.com/collections/moon

The CC0 designation applies to the downloadable assets covered by Poly Haven's
license policy. It does not automatically apply to website text, logos,
thumbnails, user gallery renders, or unrelated website content.

---

## License references

- Creative Commons Attribution 4.0 International:
  https://creativecommons.org/licenses/by/4.0/legalcode
- Creative Commons Attribution 3.0 Unported:
  https://creativecommons.org/licenses/by/3.0/legalcode
- Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International:
  https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
- Creative Commons CC0 1.0 Universal:
  https://creativecommons.org/publicdomain/zero/1.0/legalcode
- ASWF Digital Assets License v1.1:
  https://spdx.org/licenses/ASWF-Digital-Assets-1.1.html

## Redistribution requirements

1. Retain this document with the scene assets.
2. Retain every license, EULA, README, and credit file supplied in each
   original archive.
3. Retain the Bistro and Zero-Day CC BY 4.0 attribution statements, the San
   Miguel CC BY 3.0 attribution, and the Sun Temple CC BY-NC-SA 4.0
   attribution and ShareAlike terms.
4. Describe actual modifications made to redistributed CC BY or Sponza
   copies.
5. Include the Sponza copyright notice in publications containing Sponza
   renders.
6. Do not imply endorsement by any asset creator, Intel, NVIDIA, Amazon
   Lumberyard, Epic Games, Poly Haven, or their contributors.
7. Preserve each asset's original download URL, download date, archive
   filename, and checksum in its associated manifest.
