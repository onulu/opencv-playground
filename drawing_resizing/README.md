# Drawing & Resizing

## Guide

- 512x512 사이즈에서 원(마우스 오른쪽 버튼), 다각형(삼각형, 사각형 포함, 마우스 왼쪽 버튼)을 그린다.
- 리사이징 후 선 얼마나 뭉개지는지 관찰하기
- 이후 다시 부드럽게 필터링 후 축소해서(128x128) 관찰하기(CV2.INTER_AREA를 사용한것과 다른 interpoltion비교)

## Drawing

[소스코드]('./drawing.py')

**사용방법**
- `M` 키 : 원과 다각형 그리기 모드 전환
- 마우스 왼쪽 버튼: 원 그리기 / 폴리곤 시작하기
- 마우스 왼쪽 + `Shift`: 폴리곤 이어서 그리기
- 마우스 왼쪽 (no Shift): 폴리곤 닫기
- `엔터`키 : 저장
- `Esc` : 닫기

![폴리곤 그리기](/drawing_resizing/my_drawing.png)

## interpoltion 비교하기

[소스코드]('./resizing.py')

### Linear

![linear](/drawing_resizing/inter_linear.png)

### Area

![area](/drawing_resizing/inter_area.png)
