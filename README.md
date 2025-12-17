# enct

enct(encodig task)는 최적의 화질과 용량을 추정해 비디오를 인코딩하는 인코딩 자동화 도구입니다.

## Features

### 1. ffmpeg 기반 비디오 인코딩

ffmpeg에서 지원하는 다양한 인코딩 옵션들을 제공합니다.

- **최신 코덱 지원**: `HEVC (H.265)`, `AV1` 등 최신 비디오 코덱을 지원합니다.
- **GPU 가속 지원**: NVIDIA 그래픽 카드의 NVENC를 활용한 GPU 가속을 지원합니다.
- **다양하고 통일된 인코딩 옵션**
  - 해상도 및 프레임 레이트 변경, 비디오 자르기, 프레임 레이트 상한 등 다양한 인코딩 옵션을 지원합니다.
  - 인코더 종류/GPU 가속 여부에 따라 달라지는 인코딩 옵션들을 하나의 규격으로 관리할 수 있습니다.

### 2. 인코딩 퀄리티 추정 기능

목표 용량비를 기반으로 최적의 인코딩 퀄리티(e.g. CRF) 값을 추정합니다.

- (1) **임의의 퀄리티 값 지정**: 설정된 퀄리티 범위 내에서 임의의 퀄리티 값(최초의 경우 퀄리티 범위의 중앙값)을 선택합니다.
- (2) **용량비 비교**: 전체 비디오를 여러 개의 샘플로 나누고, 각 샘플들의 앞부분(x초)을 임시로 인코딩합니다. 이러한 과정을 모든 샘플에 반복해 평균 용량을 구한 뒤, 이를 원본과 비교해 용량비를 추정합니다.
- (3) **최적 퀄리티 탐색**: 목표 용량비 범위에 도달할 때까지 각 퀄리티 값에 대해 위 과정을 반복합니다. 이때 **이진 탐색 (Binary Search)** 알고리즘을 통해 효율적으로 퀄리티 값을 탐색합니다.
  - 예: 퀄리티 범위가 20~48일 때, 34, 27, 22와 같이 빠르게 범위를 좁혀가며 최적값을 찾습니다.
- (4) **모드에 따른 최종 퀄리티 결정**: 목표 용량비 범위에 해당하는 퀄리티 값을 찾은 후, 사용자가 설정한 모드에 따라 최종 퀄리티 값을 선택합니다.
  - `compression` mode: 용량비가 가장 **낮은(가장 압축률이 높은)** 퀄리티 값을 선택합니다.
  - `quality` mode: 용량비가 가장 **높은(가장 화질이 좋은)** 퀄리티 값을 선택합니다.

> 예: 목표 용량비 범위가 0.28 ~ 0.34일 경우,
> - `compression` 모드에서는 0.28에 가장 가까운 퀄리티 값을 최종적으로 선택합니다.
> - `quality` 모드에서는 0.34에 가장 가까운 퀄리티 값을 최종적으로 선택합니다.

## Configuration

프로젝트 루트에 `config.yaml` 파일을 생성하고 아래 내용을 기반으로 환경을 설정합니다.

```yaml
# --- 경로 설정 ---
srcDirPath: <원본 비디오 폴더 경로>
outDirPath: <결과물 저장 폴더 경로>
tmpDirPath: <임시 파일 생성 폴더 경로>

# --- 인코딩 설정 ---
encoding:
  enableGpu: true                                # GPU 가속 사용 여부 (true/false)
  videoCodec: av1                                # 비디오 코덱 (h265, av1 등)
  videoQuality: ~                                # 퀄리티 추정 기능을 사용할 경우 '~' 또는 비워둠
  # videoQuality: 36                             # 특정 퀄리티 값으로 고정하려면 주석 해제 후 값 입력
  videoPreset: "p4"                              # 인코딩 프리셋 (인코더에 따라 다름)
  # audioCodec: opus                             # 오디오 코덱 (선택 사항)
  # audioBitrateKb: 128k                         # 오디오 비트레이트 (선택 사항)
  # videoFrame: 30                               # 프레임 레이트 변경 (선택 사항)
  # videoMaxBitrate: 6000                        # 최대 비디오 비트레이트 (선택 사항)
  # videoScale: {width: 1280, height: 720}       # 해상도 변경 (선택 사항)
  # timeRange: {start: "30.54", end: "634.21"}   # 비디오 자르기 (선택 사항)

# --- 퀄리티 추정 기능 설정 ---
estimation:
  enabled: true                    # 퀄리티 추정 기능 활성화 여부
  request:
    priority: compression          # 우선순위 모드 (compression: 용량 우선 / quality: 화질 우선)
    qualityRange: [20, 48]         # 퀄리티 탐색 범위
    sizeRatioRange: [0.32, 0.36]   # 목표 원본 대비 용량비 범위
  sampleOption:
    size: 10                       # 비디오를 나눌 샘플 개수
    duration: "30"                 # 각 샘플에서 테스트 인코딩을 진행할 시간 (초)
```

## Quickstart

```sh
python -m venv .venv
.venv/bin/pip3 install -r requirements.txt

export CONFIG_PATH=<config.yaml path>
.venv/bin/python3 -m enct batch
```
