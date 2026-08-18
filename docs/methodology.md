# 연구 방법

## 연구 질문

Triangle Visibility Buffer는 언제 Forward/Deferred보다 유리해지는가? 이 질문을 전체 frame time 하나로 답하지 않고 다음 비용의 합으로 분해한다.

- Forward: overdraw와 quad waste가 반복시키는 material/shading 비용
- ForwardPrepass: 두 번째 geometry/rasterization 비용과 줄어든 overdraw
- Deferred: G-buffer write/read bandwidth와 geometry 비용
- VisBuf: visibility raster, fullscreen resolve, indirect vertex/index/material access
- Material Binning: histogram, prefix, flatten, class별 dispatch 비용
- 공통 비용: lighting, tonemap, presentation

## 실험 단위

각 canonical JSON은 다음 순서로 읽을 수 있게 작성한다.

1. 가설: `summary`와 spec 이름이 바꾸는 독립변수를 말한다.
2. 구현: `renderer_variant`, scene와 feature flag가 비교 계약을 고정한다.
3. 실험: `base`와 `sweep` 또는 `samples`가 조건을 완전히 기술한다.
4. 관찰: GPU timestamp CSV와 plot이 측정치를 남긴다.
5. 해석: 서로 다른 pass의 증감으로 전체 차이를 설명한다.
6. 한계: `reproduction.fidelity`, 환경 metadata와 결과 문서가 외삽 범위를 제한한다.

## 공정한 비교

- 같은 resolution, camera, scene geometry, VFC, texture loading, warm-up과 measurement frame을 사용한다.
- shared lighting/tonemap은 같은 의미로 비교하고 clear는 pass stack의 성능 주장에 포함하지 않는다.
- opaque 비교에서는 depth/visibility가 material texture를 샘플링하지 않는다.
- active material class와 material record 수를 별도 축으로 둔다.
- real-scene 성능은 fixed camera playback의 마지막 프레임까지 측정한다.
- debug renderer의 시간은 correctness 자료로만 사용하고 performance renderer와 섞지 않는다.

## 측정

`RendererBase`의 slot 0은 total GPU timestamp이며 renderer pass는 slot 1부터 기록된다. warm-up 이후 measurement frame만 통계에 들어간다. playback sidecar가 있으면 frame window와 raster workload를 별도 `frames.csv`로 정규화한다.

대표 통계는 median, average, P10/P90이다. 그래프에서 표본이 없는 구간은 보간하지 않고 비워 둔다. pass stack의 `Other`는 total에서 이름이 있는 pass 합을 뺀 값이며 음수가 되면 계측 계약을 다시 확인한다.

## Scene 전략

Synthetic scene은 geometry density, material/class count, locality, diversity, overdraw와 resolution을 독립적으로 바꾸기 위한 통제 환경이다. 실제 scene은 Sponza, Bistro, San Miguel 계열을 사용해 synthetic에서 얻은 설명이 복잡한 geometry/material distribution에서도 유지되는지 확인한다.

장면 자산은 저장소에 포함하지 않으며 경로는 machine-local config로 주입한다. 장면별 이용 조건은 `SCENE_ASSET_NOTICES.md`가 기준이다.
