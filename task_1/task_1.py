def task(array: str) -> int:
    return len(array.split('0')[0])


if __name__ == '__main__':
    print(task('111111111110000000000000000'))
