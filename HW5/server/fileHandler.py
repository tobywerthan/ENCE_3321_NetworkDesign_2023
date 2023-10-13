def fileExample():
    # Get input from user
    file_name = input("File name>")

    try:
        # Open file -> read binary
        f = open(file_name, "rb")

        # Create file -> write binary
        f2 = open("x_" + file_name, "wb")

        # Write contents to new file
        f2.write(f.read())

        # Close file
        f.close()
        f2.close()

    except FileNotFoundError as msg:
        print(str(msg))


if __name__ == "__main__":
    fileExample()
