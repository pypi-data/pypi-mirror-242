# pykma_grid
`pykma_grid`�� ������ �浵�� Lambert Conformal Conic Projection�� ����Ͽ� ���� ��ǥ�� ��ȯ�ϴ� ���̽� ��Ű���Դϴ�. �� ��Ű���� [���û API](https://www.data.go.kr/data/15084084/openapi.do)���� ����X, Y�� ����� �� �����մϴ�.

���û API ���� ���� C���� �� ���� ��ȯ �ڵ带 �ڹٽ�ũ��Ʈ�� ��ȯ�� �ڵ��Դϴ�.

## ��ġ ���
��Ű���� pip�� ����Ͽ� ���� ��ġ�� �� �ֽ��ϴ�:

```shell
pip install pykma_grid
```

## �⺻ ��� ���
`pykma_grid` ��Ű���� ����ϱ� ���ؼ���, ���� `Coordinate` Ŭ������ ����Ʈ�ϰ� ���� �� �浵 ���� ���ڷ� �����Ͽ� �ν��Ͻ��� �����մϴ�. �� ��, `gridX`�� `gridY` �Ӽ��� ����Ͽ� ���� ��ǥ�� ���� �� �ֽ��ϴ�.

```python
from pykma_grid import Coordinate

coord = Coordinate(37.565, 126.9780)

print("Grid X:", coord.gridX)
print("Grid Y:", coord.gridY)
```

## API ����
### `Coordinate(latitude, longitude)`
- `latitude` (float): ���� (degrees)
- `longitude` (float): �浵 (degrees)

### �Ӽ�
- `gridX`: ���� X ��ǥ�� ��ȯ�մϴ� (float).
- `gridY`: ���� Y ��ǥ�� ��ȯ�մϴ� (float).

## ���̼���
�� ������Ʈ�� MIT ���̼����� �����ϴ�. ���̼����� ���� �ڼ��� ������ LICENSE ������ �������ּ���.

## �⿩
�⿩�� ���Ͻø� ������Ʈ�� GitHub ����ҿ� pull request�� �����ֽðų� �̽��� ������ּ���.

## ����
�����̳� ���� ������ �����ø� �̽��� ���� �ֽñ� �ٶ��ϴ�.
