# De-noising

## Image 01: no mask

1. `Bilateral` 필터를 적용하여 에지를 보존하면서 초기 노이즈를 제거
2. `Unsharp Masking`: 원본과 Bilateral 필터링 결과를 이용해 이미지 선명화
3. `fastNlMeansDenoisingColored` 함수를 사용하여 컬러 노이즈 제거
4. `Gaussian Blur`로 하늘의 잔여 노이즈를 부드럽게 제거
5. `convertScaleAbs` 함수로 대비는 10% 증가, 밝기는 약간 감소

Before
![대체 iamge1](/denoising/img/01.png)

After
![대체 iamge1](/denoising/img/result_nomask_01.png)

## Image 01: with mask

1. 그레이스케일로 변환 후 이진화하여 마스크를 생성
2. 모폴로지 연산으로 마스크를 정제: 하늘과 건물 부분을 분리
3. 하늘 부분에 `bilateral` 필터와 `fastNlMeansDenoisingColored` 필터를 적용하여 노이즈를 제거
4. 처리된 하늘 부분과 원본 건물 부분을 다시 합침
5. 전체 이미지의 밝기를 낮추고 대비를 조정

Before
![대체 iamge1](/denoising/img/01.png)

After: masking
![대체 iamge1](/denoising/img/result_01.png)

## Image 02

1. `fastNlMeansDenoisingColored` 함수를 사용하여 컬러 이미지의 노이즈를 제거
2. `3x3` 커널을 사용한 `High-Pass` 필터로 이미지 선명도 조절
3. 블렌딩: 노이즈가 제거된 이미지(70%)와 선명화된 이미지(30%)를 혼합

Before
![대체 iamge2](/denoising/img/03.png)

After
![대체 iamge2](/denoising/img/result_02.png)

## Image 03

1. `fastNlMeansDenoisingColored` 함수를 사용하여 컬러 이미지의 노이즈를 제거
2. `convertScaleAbs`를 사용해 밝기, 컨트라스트 조절
3. `3x3` 커널을 사용한 `High-Pass` 필터로 이미지 선명도 조절

Before
![대체 iamge1](/denoising/img/05.png)

After
![대체 iamge1](/denoising/img/result_03.png)

---

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
