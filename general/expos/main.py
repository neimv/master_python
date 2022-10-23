
import argparse


class IrisClass:
    def __init__(
        self,
        sepal_length: str,
        sepal_width: str,
        petal_length: str,
        petal_width: str,
        class_type: str
    ) -> None:
        self.sepal_length = float(sepal_length)
        self.sepal_width = float(sepal_width)
        self.petal_length = float(petal_length)
        self.petal_width = float(petal_width)
        self.class_type = class_type

    def transform_class_type(self) -> str:
        mapper = {
            "Iris-setosa": 1,
            "Iris-versicolor": 2,
            "Iris-virginica": 3,
        }
        n_class_type = mapper[self.class_type]

        return (
            f'{self.sepal_length},'
            f'{self.sepal_width},'
            f'{self.petal_length},'
            f'{self.petal_width},'
            f'{n_class_type}'
        )

    def __str__(self) -> str:
        return (
            f'Class Flower: {self.class_type}\n'
            f'Sepal Size: [{self.sepal_length}, {self.sepal_width}]\n'
            f'Petal Size: [{self.petal_length}, {self.petal_width}]\n'
        )

    def __repr__(self) -> str:
        return (
            f'Class Flower: {self.class_type}\n'
            f'Sepal Length: {self.sepal_length}\n'
            f'Sepal Width: {self.sepal_width}\n'
            f'Petal Length: {self.petal_length}\n'
            f'Petal Width: {self.petal_width}\n'
        )


def file_open_old(
    name: str,
    mode: str,
    encoding: str = "utf-8",
    full: bool = False
):
    f = open(name, mode, encoding=encoding)
    read_file(f)
    f.close()


def file_open_context(name: str, mode: str, encoding: str = "utf-8"):
    pass


def write_file(file_buffer):
    pass


def read_file(file_buffer):
    flowers = []

    for line in file_buffer:
        line_split = line.replace('\n', '').split(',')
        # print(line_split)

        if len(line_split) == 5:
            iris_flower = IrisClass(
                line_split[0],
                line_split[1],
                line_split[2],
                line_split[3],
                line_split[4],
            )
            print(str(iris_flower))
            print(iris_flower.transform_class_type())
            # flowers.append(iris_flower)


def main(argument):
    pass


if __name__ == "__main__":
    file_open_old('iris.data', 'r')

