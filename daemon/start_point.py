import daemon


def main():
    order = daemon.get_order_messege_queue()
    daemon.write_into_db(order)

    print("FINISHED")


if __name__ == '__main__':
    main()
