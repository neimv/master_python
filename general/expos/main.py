
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
            "Iris-setosa": 0,
            "Iris-versicolor": 1,
            "Iris-virginica": 2,
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
    __file_works(name, mode, f, full)
    f.close()


def file_open_context(
    name: str,
    mode: str,
    encoding: str = "utf-8",
    full: bool = False
):
    pass


def write_file(file_name, mode, file_buffer, data=None, encoding='utf-8'):
    file_name = f'{file_name}_backup.csv'
    if data is not None:
        with open(file_name, 'w', encoding=encoding) as file_bk:
            for flower in data:
                file_bk.write(flower.transform_class_type())
                file_bk.write('\n')
    else:
        while True:
            writer = input(
                "Want do you write in the document? (-1 to exit)>> "
            )

            if writer == "-1":
                break

            file_buffer.write(writer + "\n")


def read_file(file_buffer, full: bool) -> list:
    flowers = []
    file_buffer = file_buffer.readlines() if full else file_buffer

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
            flowers.append(iris_flower)

    return flowers


def __file_works(name: str, mode: str, file_work, full):
    if mode == 'r':
        flowers = read_file(file_work, full)

        for flower in flowers:
            print(flower)
    elif mode == 'w':
        write_file(name, mode, file_work)
    elif mode == 'a':
        pass
    elif mode == 'x':
        pass
    elif mode == 'w+':
        pass
    elif mode == 'r+':
        flowers = read_file(file_work, full)
        write_file(name, mode, file_work, flowers)


def main(argument):
    pass


if __name__ == "__main__":
    file_open_old('iris.data', 'w', full=False)
