# Third-Party Software Notices

This file records third-party source code, shader code, libraries, and build
dependencies used by VisibilityBufferInfo. Scene assets are documented
separately in [SCENE_ASSET_NOTICES.md](SCENE_ASSET_NOTICES.md).

The project-level [LICENSE](LICENSE) applies only to material authored for this
project. It does not override any copyright notice or license listed here or
embedded in an individual file.

## Dependency inventory

| Component | Version / revision | How it is used | License |
|---|---|---|---|
| DirectXTex | `may2026` | Fetched by CMake and linked statically | MIT |
| fastgltf | `v0.9.0` | Fetched by CMake and linked statically | MIT |
| DirectX Shader Compiler (DXC) | NuGet `Microsoft.Direct3D.DXC` `1.8.2505.32` | `dxcompiler.dll` and `dxil.dll` are copied to the runtime directory | Package metadata names the University of Illinois/NCSA license; the package also includes Microsoft and MIT license files |
| Assimp | `v5.4.3` | Fetched by CMake, built statically, and used for scene import | BSD 3-Clause; the verified Windows build also compiles Clipper, Open3DGC, OpenDDLParser, Poly2Tri, MiniZip/unzip, and zlib under their own licenses |
| NVIDIA Donut shader code | Exact upstream commit was not recorded when copied | Shader files copied or adapted under `assets/shaders/donut/` and `assets/shaders/mydonut/` | MIT; retain every NVIDIA file header |
| simdjson | `v3.12.3` | Downloaded as single-header source by fastgltf `v0.9.0` | Apache License 2.0; embedded third-party notices remain in the generated source |
| zlib | Assimp `v5.4.3` bundled copy | Built by Assimp | zlib License |

NVRHI is neither vendored nor linked by the current source tree. Donut uses
NVRHI upstream, but this project contains selected Donut-derived shaders, not
the Donut or NVRHI runtime libraries.

## Redistribution checklist

- Keep this file and all per-file copyright headers with source releases.
- Keep `LICENSE`, `THIRD_PARTY_NOTICES.md`, and the exact DXC package license
  files with binary releases.
- The CMake runtime deployment copies the DXC package's `LICENSE-LLVM.txt`,
  `LICENSE-MS.txt`, `LICENCE-MIT.txt`, and `distributable_files.txt` beside the
  runtime legal notices. Do not remove them from a redistributed build.
- If a local Assimp checkout is substituted through
  `TVBPERF_ASSIMP_LOCAL_SOURCE`, audit that checkout's version and license tree;
  this notice describes the default fetched `v5.4.3` configuration.
- Retain license and notice files contained in any fetched source tree when
  redistributing that source tree. In particular, Assimp's `contrib/` folder
  and simdjson's generated single-header source contain additional notices.

## DirectXTex

Source: https://github.com/microsoft/DirectXTex/tree/may2026

Copyright (c) Microsoft Corporation.

Licensed under the MIT License reproduced in the Common MIT License section.

## fastgltf

Source: https://github.com/spnda/fastgltf/tree/v0.9.0

Copyright (c) 2022-2025 Sean Apeler. All rights reserved.

Licensed under the MIT License reproduced in the Common MIT License section.

### simdjson fetched by fastgltf

Source: https://github.com/simdjson/simdjson/tree/v3.12.3

Copyright 2018-2025 The simdjson authors.

Licensed under the Apache License, Version 2.0. The complete license is
reproduced below and is available at
https://www.apache.org/licenses/LICENSE-2.0. The single-header files downloaded
by fastgltf retain embedded notices for code incorporated by simdjson.

### Apache License 2.0

Copyright 2018-2025 The simdjson authors

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0.

Apache License

Version 2.0, January 2004

http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

   "License" shall mean the terms and conditions for use, reproduction, and
   distribution as defined by Sections 1 through 9 of this document.

   "Licensor" shall mean the copyright owner or entity authorized by the
   copyright owner that is granting the License.

   "Legal Entity" shall mean the union of the acting entity and all other
   entities that control, are controlled by, or are under common control with
   that entity. For the purposes of this definition, "control" means (i) the
   power, direct or indirect, to cause the direction or management of such
   entity, whether by contract or otherwise, or (ii) ownership of fifty percent
   (50%) or more of the outstanding shares, or (iii) beneficial ownership of
   such entity.

   "You" (or "Your") shall mean an individual or Legal Entity exercising
   permissions granted by this License.

   "Source" form shall mean the preferred form for making modifications,
   including but not limited to software source code, documentation source, and
   configuration files.

   "Object" form shall mean any form resulting from mechanical transformation
   or translation of a Source form, including but not limited to compiled
   object code, generated documentation, and conversions to other media types.

   "Work" shall mean the work of authorship, whether in Source or Object form,
   made available under the License, as indicated by a copyright notice that is
   included in or attached to the work.

   "Derivative Works" shall mean any work, whether in Source or Object form,
   that is based on (or derived from) the Work and for which the editorial
   revisions, annotations, elaborations, or other modifications represent, as a
   whole, an original work of authorship. For the purposes of this License,
   Derivative Works shall not include works that remain separable from, or
   merely link (or bind by name) to the interfaces of, the Work and Derivative
   Works thereof.

   "Contribution" shall mean any work of authorship, including the original
   version of the Work and any modifications or additions to that Work or
   Derivative Works thereof, that is intentionally submitted to Licensor for
   inclusion in the Work by the copyright owner or by an individual or Legal
   Entity authorized to submit on behalf of the copyright owner. For the
   purposes of this definition, "submitted" means any form of electronic,
   verbal, or written communication sent to the Licensor or its representatives,
   including but not limited to communication on electronic mailing lists,
   source code control systems, and issue tracking systems that are managed by,
   or on behalf of, the Licensor for the purpose of discussing and improving
   the Work, but excluding communication that is conspicuously marked or
   otherwise designated in writing by the copyright owner as "Not a
   Contribution."

   "Contributor" shall mean Licensor and any individual or Legal Entity on
   behalf of whom a Contribution has been received by Licensor and subsequently
   incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of this
   License, each Contributor hereby grants to You a perpetual, worldwide,
   non-exclusive, no-charge, royalty-free, irrevocable copyright license to
   reproduce, prepare Derivative Works of, publicly display, publicly perform,
   sublicense, and distribute the Work and such Derivative Works in Source or
   Object form.

3. Grant of Patent License. Subject to the terms and conditions of this
   License, each Contributor hereby grants to You a perpetual, worldwide,
   non-exclusive, no-charge, royalty-free, irrevocable (except as stated in
   this section) patent license to make, have made, use, offer to sell, sell,
   import, and otherwise transfer the Work, where such license applies only to
   those patent claims licensable by such Contributor that are necessarily
   infringed by their Contribution(s) alone or by combination of their
   Contribution(s) with the Work to which such Contribution(s) was submitted.
   If You institute patent litigation against any entity (including a
   cross-claim or counterclaim in a lawsuit) alleging that the Work or a
   Contribution incorporated within the Work constitutes direct or
   contributory patent infringement, then any patent licenses granted to You
   under this License for that Work shall terminate as of the date such
   litigation is filed.

4. Redistribution. You may reproduce and distribute copies of the Work or
   Derivative Works thereof in any medium, with or without modifications, and
   in Source or Object form, provided that You meet the following conditions:

   a. You must give any other recipients of the Work or Derivative Works a copy
      of this License; and

   b. You must cause any modified files to carry prominent notices stating that
      You changed the files; and

   c. You must retain, in the Source form of any Derivative Works that You
      distribute, all copyright, patent, trademark, and attribution notices
      from the Source form of the Work, excluding those notices that do not
      pertain to any part of the Derivative Works; and

   d. If the Work includes a "NOTICE" text file as part of its distribution,
      then any Derivative Works that You distribute must include a readable
      copy of the attribution notices contained within such NOTICE file,
      excluding those notices that do not pertain to any part of the Derivative
      Works, in at least one of the following places: within a NOTICE text file
      distributed as part of the Derivative Works; within the Source form or
      documentation, if provided along with the Derivative Works; or, within a
      display generated by the Derivative Works, if and wherever such
      third-party notices normally appear. The contents of the NOTICE file are
      for informational purposes only and do not modify the License. You may
      add Your own attribution notices within Derivative Works that You
      distribute, alongside or as an addendum to the NOTICE text from the Work,
      provided that such additional attribution notices cannot be construed as
      modifying the License.

   You may add Your own copyright statement to Your modifications and may
   provide additional or different license terms and conditions for use,
   reproduction, or distribution of Your modifications, or for any such
   Derivative Works as a whole, provided Your use, reproduction, and
   distribution of the Work otherwise complies with the conditions stated in
   this License.

5. Submission of Contributions. Unless You explicitly state otherwise, any
   Contribution intentionally submitted for inclusion in the Work by You to the
   Licensor shall be under the terms and conditions of this License, without
   any additional terms or conditions. Notwithstanding the above, nothing
   herein shall supersede or modify the terms of any separate license agreement
   you may have executed with Licensor regarding such Contributions.

6. Trademarks. This License does not grant permission to use the trade names,
   trademarks, service marks, or product names of the Licensor, except as
   required for reasonable and customary use in describing the origin of the
   Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty. Unless required by applicable law or agreed to in
   writing, Licensor provides the Work (and each Contributor provides its
   Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied, including, without limitation, any
   warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or
   FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining
   the appropriateness of using or redistributing the Work and assume any risks
   associated with Your exercise of permissions under this License.

8. Limitation of Liability. In no event and under no legal theory, whether in
   tort (including negligence), contract, or otherwise, unless required by
   applicable law (such as deliberate and grossly negligent acts) or agreed to
   in writing, shall any Contributor be liable to You for damages, including
   any direct, indirect, special, incidental, or consequential damages of any
   character arising as a result of this License or out of the use or inability
   to use the Work (including but not limited to damages for loss of goodwill,
   work stoppage, computer failure or malfunction, or any and all other
   commercial damages or losses), even if such Contributor has been advised of
   the possibility of such damages.

9. Accepting Warranty or Additional Liability. While redistributing the Work
   or Derivative Works thereof, You may choose to offer, and charge a fee for,
   acceptance of support, warranty, indemnity, or other liability obligations
   and/or rights consistent with this License. However, in accepting such
   obligations, You may act only on Your own behalf and on Your sole
   responsibility, not on behalf of any other Contributor, and only if You
   agree to indemnify, defend, and hold each Contributor harmless for any
   liability incurred by, or claims asserted against, such Contributor by
   reason of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS

### Notices embedded in simdjson's single-header distribution

`string-view lite` is Copyright 2017-2020 Martin Moene and is distributed under
the Boost Software License 1.0:

> Boost Software License - Version 1.0 - August 17th, 2003
>
> Permission is hereby granted, free of charge, to any person or organization
> obtaining a copy of the software and accompanying documentation covered by
> this license (the "Software") to use, reproduce, display, distribute,
> execute, and transmit the Software, and to prepare derivative works of the
> Software, and to permit third-parties to whom the Software is furnished to do
> so, all subject to the following:
>
> The copyright notices in the Software and this entire statement, including
> the above license grant, this restriction and the following disclaimer, must
> be included in all copies of the Software, in whole or in part, and all
> derivative works of the Software, unless such copies or derivative works are
> solely in the form of machine-executable object code generated by a source
> language processor.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
> SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR
> ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
> ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
> DEALINGS IN THE SOFTWARE.

simdjson's instruction-set detection contains highly modified code originating
from PyTorch. Its embedded notice is reproduced below.

Copyright (c) 2016- Facebook, Inc. (Adam Paszke)

Copyright (c) 2014- Facebook, Inc. (Soumith Chintala)

Copyright (c) 2011-2014 Idiap Research Institute (Ronan Collobert)

Copyright (c) 2012-2014 Deepmind Technologies (Koray Kavukcuoglu)

Copyright (c) 2011-2012 NEC Laboratories America (Koray Kavukcuoglu)

Copyright (c) 2011-2013 NYU (Clement Farabet)

Copyright (c) 2006-2010 NEC Laboratories America (Ronan Collobert, Leon
Bottou, Iain Melvin, Jason Weston)

Copyright (c) 2006 Idiap Research Institute (Samy Bengio)

Copyright (c) 2001-2004 Idiap Research Institute (Ronan Collobert, Samy
Bengio, Johnny Mariethoz)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the names of Facebook, Deepmind Technologies, NYU, NEC Laboratories
   America and IDIAP Research Institute nor the names of its contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## DirectX Shader Compiler

Package: https://www.nuget.org/packages/Microsoft.Direct3D.DXC/1.8.2505.32

Source: https://github.com/microsoft/DirectXShaderCompiler

The NuGet package declares `LICENSE-LLVM.txt` as its license file and contains
these additional unmodified legal files:

- `LICENSE-MS.txt`
- `LICENCE-MIT.txt`
- `distributable_files.txt`

The package's distributable list explicitly includes `dxcompiler.dll` and
`dxil.dll`, which are the two files deployed by this project. The original
package files copied into a build are authoritative if this summary differs.

### University of Illinois/NCSA license from `LICENSE-LLVM.txt`

Copyright (c) 2003-2015 University of Illinois at Urbana-Champaign.
All rights reserved.

Developed by the LLVM Team, University of Illinois at Urbana-Champaign.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal with
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimers.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimers in the documentation
  and/or other materials provided with the distribution.
- Neither the names of the LLVM Team, University of Illinois at
  Urbana-Champaign, nor the names of its contributors may be used to endorse or
  promote products derived from this Software without specific prior written
  permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

## Assimp

Source: https://github.com/assimp/assimp/tree/v5.4.3

Open Asset Import Library (assimp)

Copyright (c) 2006-2021, assimp team. All rights reserved.

Redistribution and use of this software in source and binary forms, with or
without modification, are permitted provided that the following conditions are
met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the assimp team, nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission of the assimp team.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Assimp's root license also contains this separate notice for Poly2Tri:

Poly2Tri Copyright (c) 2009-2010, Poly2Tri Contributors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of Poly2Tri nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific
  prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Any source distribution must retain the complete upstream `LICENSE` file and
the individual license files under `contrib/`. Assimp test models are not
copied into this repository or runtime output.

### Other Assimp components compiled by the verified Windows build

- Clipper is distributed under the Boost Software License 1.0 reproduced in
  the simdjson section above.
- OpenDDLParser is Copyright (c) 2014 Kim Kulling and is distributed under the
  MIT License reproduced in the Common MIT License section.
- Most Open3DGC files are Copyright (c) 2013 Khaled Mammou - Advanced Micro
  Devices, Inc. and are distributed under the MIT License reproduced in the
  Common MIT License section.
- Open3DGC's arithmetic codec is Copyright (c) 2004 Amir Said and William A.
  Pearlman. Its BSD-style terms are reproduced below.
- MiniZip/unzip is Copyright (c) 1998-2010 Gilles Vollant, with Zip64
  modifications Copyright (c) 2007-2008 Even Rouault and Copyright (c)
  2009-2010 Mathias Svensson. It uses the zlib terms reproduced below.

Open3DGC arithmetic codec notice:

Copyright (c) 2004 Amir Said and William A. Pearlman. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### zlib bundled by Assimp

Copyright (c) 1995-2022 Jean-loup Gailly and Mark Adler.

This software is provided "as-is", without any express or implied warranty. In
no event will the authors be held liable for any damages arising from the use
of this software.

Permission is granted to anyone to use this software for any purpose, including
commercial applications, and to alter it and redistribute it freely, subject
to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim
   that you wrote the original software. If you use this software in a product,
   an acknowledgment in the product documentation would be appreciated but is
   not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

## NVIDIA Donut-derived shader code

Upstream source: https://github.com/NVIDIA-RTX/Donut

The original import is recorded in this repository's history, but it did not
record an exact Donut commit. Therefore the copyright header in each copied
file is the authoritative provenance record. Files under
`assets/shaders/donut/` retain their original headers. The adapted
`assets/shaders/mydonut/donut_gbuffer_PS.hlsl` and
`assets/shaders/mydonut/donut_gbuffer_VS.hlsl` also retain the NVIDIA header
from their source lineage.

Copyright notices vary by upstream file and include:

- Copyright (c) 2014-2021, NVIDIA CORPORATION. All rights reserved.
- Copyright (c) 2014-2024, NVIDIA CORPORATION. All rights reserved.
- Copyright (c) 2016-2017 Gary Hsu, for PBR workflow conversion code retained
  in `assets/shaders/donut/donut_scene_material.hlsli`.

These portions are licensed under the MIT License reproduced below.

## Common MIT License text

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
