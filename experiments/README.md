# Experiment catalog

이 폴더는 결과가 아니라 결과를 만드는 선언을 저장한다.

```text
camera_paths/       fixed playback CSV
specs/              canonical experiment JSON
suites/             named spec collections
schema.json         experiment shape
plot_theme.json     renderer/pass visual grammar
local.example.json  machine-local path template
```

## Spec 작성

필수 metadata는 `schema_version`, `id`, `title`, `executable`, `reproduction`, `base`, `analysis`다. parameter variation은 Cartesian product가 필요하면 `sweep`, 직접 고른 condition이면 `samples`를 사용한다. 두 필드를 동시에 쓰지 않는다.

`base`, `sweep`, `samples`의 key는 `include/ProgramArgument.h`와 일치해야 한다. `_`로 시작하는 key는 주석용이며 runner가 무시한다. 재현 가능한 spec은 C++ 기본값에 기대지 않고 camera, warm-up, measurement, VSync, VFC, texture와 renderer 조건을 명시한다.

Plot 예:

```json
{
  "analysis": {
    "plots": [
      {"id": "total_time", "type": "total", "metric": "total_time_median_ms"},
      {"id": "pass_breakdown", "type": "pass_breakdown"}
    ]
  }
}
```

## 명령

```powershell
python scripts/reproduce.py --verify
python scripts/reproduce.py --suite smoke --build --overwrite
python scripts/reproduce.py --spec experiments/specs/synthetic/followup_01_synth_decoupling_smoke.json --overwrite
```

결과 위치는 spec의 `id`와 같으며 `results/<id>/` 아래에 만들어진다.
