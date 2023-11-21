from generic_scpi_driver import get_controller_func

from .driver import _TTIPowerSupplyBase

main = get_controller_func("TTIPowerSupply", 3301, _TTIPowerSupplyBase)


if __name__ == "__main__":
    main()
