# 실험 이관 상태

## 결과 파일에서 실행 정의로

과거 `datas/`, `scripts/results/`와 dashboard data에는 JSON, CSV, plot script, PNG, 실패 기록과 복사본이 같은 층위로 섞여 있었다. 이관 과정에서는 실행 가능한 의미만 canonical spec으로 올리고 결과물은 `results/`에서 다시 생성하도록 바꿨다.

현재 상태:

| 분류 | Spec | Runs | 의미 |
|---|---:|---:|---|
| exact | 57 | canonical inventory에 포함 | 현재 인자만으로 과거 조건을 그대로 표현 |
| adapted | 9 | canonical inventory에 포함 | 제거된 인자 또는 현재 renderer 계약에 맞춰 가장 가까운 조건으로 조정 |
| 합계 | 66 | 4,280 | `--verify`로 정적 검증 |

초기 `experiments_1` 결과처럼 원본 runner spec과 인자 계약을 복원할 수 없는 자료, backup/result copy, 실패 전용 결과는 canonical 실험으로 가장하지 않았다. 대응 가능한 후속 실험이 있으면 그 spec으로 대체하고, 없으면 이관을 포기했다.

각 spec의 `reproduction`은 `fidelity`, `legacy_source`, 필요한 경우 `note`를 가진다. `legacy_source`는 출처 추적용 문자열이며 실행 시 해당 파일을 요구하지 않는다.

## Suite

- `smoke`: build와 runner 계약을 빠르게 확인하는 6 synthetic runs
- `portfolio`: material, real scene, validation, capture의 대표 evidence set
- `all`: 66개 spec 전체, 4,280 runs

`--dry-run`은 executable이나 scene을 열지 않고 확장된 run 수만 확인한다.

## Plot 선언

각 JSON의 `analysis.plots`는 필요한 시각화를 선언한다. 공통 generator가 지원하는 유형은 total/line, grouped bar, pass breakdown, scatter, heatmap이다. 개별 실험 폴더에 plot script를 복제하지 않는다.

색상은 `experiments/plot_theme.json`의 단일 계약을 따른다.

- Forward: blue
- Deferred: orange
- VisBuf: green
- pre-pass/visibility: light tone
- geometry/shading: medium tone
- lighting/resolve: dark tone
- material utility: yellow
- shared: purple
- unmeasured remainder: gray

PNG와 SVG를 함께 만들며 plot manifest가 생성 파일과 성공/skip 상태를 기록한다.
