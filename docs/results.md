# 대표 결과와 해석

## 범위

아래 수치는 2026-07-30 후속 캠페인의 RTX 5060 Ti 16GB 결과다. Release/Ninja/MSVC build에서 Donut DeferredPrepass(variant 8)와 Donut VisBuf+G-buffer(variant 9)를 같은 opaque 계약으로 비교했다. 17개 config, 1,301 runs가 모두 success였고 salvaged/failed/skipped는 0이었다.

이전 RTX 5070 자료는 하드웨어가 다르므로 절대 시간을 합치거나 평균내지 않았다.

## 가설 1: material record보다 active class scheduling이 중요하다

### 구현과 실험

Deferred와 VisBuf가 같은 수의 generic shader class를 선택할 기회를 갖게 하고, material count와 active class count를 독립적으로 sweep했다.

### 관찰

- 한 class에 모든 material을 매핑했을 때 material 1→255 변화는 Deferred 0.243→0.252 ms, VisBuf 0.318→0.329 ms였다.
- 255 materials에서 class 1→255 변화는 Deferred 0.281→0.280 ms, VisBuf 0.344→0.562 ms였다.
- material × class 45개 sampled cell은 모두 Deferred가 빨랐다.

### 해석

현재 VisBuf의 주된 material 관련 병목은 record 수 자체보다 histogram/prefix/flatten과 class별 dispatch에 있다. 이는 specialized material shader의 일반적 가치가 아니라 현재 generic binning 구현의 scheduling cost에 대한 결과다.

### 한계

class마다 정적으로 다른 shader body를 사용하지 않는다. 따라서 material specialization이 주는 branch/occupancy 이득까지 평가한 결과로 해석하면 안 된다.

## 가설 2: geometry가 무거워지면 VisBuf의 고정 비용이 상쇄된다

### 구현과 실험

Synthetic geometry density, resolution, locality/diversity와 20 paired seeds를 각각 sweep했다.

### 관찰

- 가장 무거운 sampled geometry 조건에서 Deferred/VisBuf ratio는 0.916으로 parity에 가장 가까웠지만 crossover는 없었다.
- 0.5184–8.2944 megapixels 범위의 ratio는 0.576–0.734였다.
- 20 seeds의 평균 ratio는 0.6886, sample standard deviation은 0.0117이었다.
- 9×9 locality/diversity map 81 cells에서도 equal-time crossover는 없었다.

### 해석

geometry workload가 커질수록 VisBuf의 고정 resolve/binning 비용은 상대적으로 작아진다. 다만 현재 sampled 범위는 crossover를 보여 주지 못했다.

### 한계

`geometry_div=256`보다 높은 targeted sweep과 여러 process repeat가 필요하다. Nsight/PIX hardware counter가 없으므로 cache나 occupancy를 원인으로 단정하지 않는다.

## 가설 3: 실제 scene에서는 pass별 상쇄가 승패를 결정한다

### 관찰

| Scene | DeferredPrepass avg | VisBuf avg | Deferred / VisBuf |
|---|---:|---:|---:|
| Sponza | 1.17241 ms | 1.76071 ms | 0.6659 |
| Sponza + Ivy | 1.68781 ms | 2.07718 ms | 0.8125 |
| Bistro | 0.53941 ms | 0.66268 ms | 0.8140 |

- Sponza에서 Deferred geometry+depth는 1.028 ms, VisBuf compute G-buffer는 1.319 ms였다. visibility 0.222 ms와 binning 0.067 ms가 추가됐다.
- Sponza + Ivy에서 compute G-buffer는 geometry+depth보다 0.225 ms 저렴했지만 visibility+binning 0.609 ms가 이를 뒤집었다.
- Bistro에서도 compute G-buffer가 0.175 ms를 절약했지만 visibility+binning이 약 0.285 ms였다.
- lighting과 tonemap은 renderer 사이에서 비슷했다.

### 해석

현재 구현의 개선 우선순위는 shared lighting이 아니라 visibility raster, class scheduling과 compute reconstruction/access다. VisBuf가 geometry/G-buffer 비용을 실제로 줄인 장면에서도 그 절약만 보고 전체 승리를 예측할 수 없다.

### 한계

complete-camera 조건은 frame sample은 많지만 scene/renderer 조건당 process repeat가 하나다. GPU가 바뀌면 같은 spec을 다시 실행해야 한다.

## 정확성 검증

Raster reference와 VisBuf reconstruction 910 frame pair에서 평균 interior MAE는 8-bit 기준 0.018412 LSB, bit-exact interior channel은 98.3831%, 평균 coverage mismatch는 0%였다. linear/perspective barycentric, barycentric derivative, UV derivative와 texture LOD proxy를 별도 debug mode로 비교했다.

이 결과는 analytic reconstruction이 sampled opaque 장면에서 raster reference와 매우 가깝다는 증거다. 성능 renderer의 visual correctness 전체를 보증하거나 alpha blend, transmission, shadow, IBL까지 검증한 것은 아니다.

## 다음 실험

1. geometry density를 현재 최대보다 높여 crossover 존재 여부를 찾는다.
2. complete camera를 process-level repeat해 run-to-run variance를 얻는다.
3. 대표 camera window를 Nsight/PIX로 측정해 cache, wave occupancy와 bandwidth 가설을 검증한다.
4. generic class scheduling과 실제 specialized material shader를 분리해 측정한다.
5. alpha-tested geometry는 opaque 계약에 섞지 않고 별도 benchmark로 만든다.
