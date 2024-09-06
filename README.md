# opencv-playground

## De-noising techniques

### Bilateral Filter

- Bilateral Filter(양방향 필터)는 외곽을 유지하면서 노이즈 제거에 유용함.
- 양방향 필터는 픽셀 간의 공간적 근접성과 강도 유사성을 모두 고려하여 작동한다.
- 픽셀의 강도를 주변 픽셀의 강도 값을 가중치 평균으로 대체함.

#### 파라미터

- `d` (Diameter): 이웃 픽셀의 사이즈. 클수록 블러 영역이 커지고 계산비용 증가. 보통 5-9값을 사용함
- `sigmaColor`: 값이 클수록 더 넓은 강도 범위에서 색상을 혼합할 수 있고 값이 작을수록 가장자리를 더 엄격하게 보존. (10-150)
- `sigmaSpace`: 공간 거리가 얼마나 영향을 미치는지 제어. 값이 클수록 더 넓은 영역의 픽셀을 혼합한다.(10-150, 시그마컬러와 비슷하게 설정함)

- 디테일이 많은 이미지에서는 `d`와 `sigmaColor값을` 줄인다.
- 노이즈가 많은 이미지에서는 `sigmaColor`, `sigmaSpace` 값을 높여본다.
- 고해상도 이미지에서는 `d`사이즈를 줄인다.

```python
bilateral = cv2.bilateralFilter(src=img, d=9, sigmaColor=50, sigmaSpace=30)
```

### Non-Local Means De-noising

- openCV에서는 `fastNlMeansDenoisingColored` 필터를 사용하여 적용가능
- 이미지에서 유사한 패치를 사용하여 서로의 노이즈를 제거한다.
- 가까운 픽셀만 고려하는 로컬 방식과 달리 NLM은 전체 이미지에서 유사한 패치를 검색한다.
- 노이즈 제거시 텍스처와 미세한 디테일을 보존하는데 효과적이다,

#### 파라미터

- `h`: luminance 강도 (보통 3-20)
  - Y채널 (밝기)에 영향을 줄 수 있다.
- `hColor`: color의 강도 (보통 3-20)
  - 컬러에 대한 노이즈 제거를 조절.
  - 일반적으로 h보다 같거나 적은 값을 적용.
  - 값이 높을수록 칼라 노이즈 제거에 효과적이나 컬러번짐 발생.
- `templateWindowSize`: 패치 사이즈 (디폴트 7)
- `searchWindowSize`: 비슷한 패치 검색을 위한 윈도우 크기 (디폴트 21)
  
```python
nl_means = cv2.fastNlMeansDenoisingColored(bilateral, None, h=10, hColor=10)
```

### Sharpening

#### Unsharp masking

- 가장 일반적인 방법으로 원본이미지에서 블러된 버전을 빼서 윤곽(edge)를 강조한다.
- 이 차이에 다시 원본을 더해 선명도를 높인다.

```python
kernel_size=(5,5) # 블러의 범위. (야간 사진에서는 3,3의 작은 사이즈)
sigma = 1.0 # Gaussian blur의 강조
amount = 1.0 # 선명도의 강도, 높을수록 선명해지지만 노이즈도 증가
blurred = cv2.GaussianBlur(image, kernel_size, sigma)
sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
```

#### High-Pass Filter

- 높은 주파수(급격한 변화)는 통과하고 낮은 주파수(부드러운 변화)는 통과하지 못하게 해 고주파 성분을 강조하는 기법.
- 주로 세부정보를 강조하는 데 사용된다.
- 커널은 중앙 값이 양수이고 주변 값이 음수인 행렬로 convolution operation을 통해 적용된다.
- 커널의 중앙 값을 조정하여 선명화 강도를 제어할 수 있다.

```python
# 가장 일반적인 커널의 형태
# 중앙값 9가 주변값의 합 -8보다 크므로 고주파를 강조한다.
# 모든 값의 합이 1이므로 전체 이미지의 밝기를 유지한다.
[[-1, -1, -1],
 [-1,  9, -1],
 [-1, -1, -1]]
```

```python
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpened = cv2.filter2D(image, -1, kernel)
```
