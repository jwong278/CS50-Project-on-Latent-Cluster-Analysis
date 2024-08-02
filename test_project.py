from project import check_file, check_table, check_cluster
import pandas as pd
import pytest

def test_check_file():
    with pytest.raises(ValueError):
        check_file("/workspaces/147152992/project/wrongfile.csv")

    with pytest.raises(ValueError):
        check_file("/wrongpath/Data.csv")

    with pytest.raises(ValueError):
        check_file("/workspaces/147152992/project/data.xls")

    with pytest.raises(ValueError):
        check_file("/workspaces/147152992/project/data.txt")

def test_check_table():
    with pytest.raises(KeyError):
        check_table("wrong.csv")

    with pytest.raises(ValueError):
        check_table("wrong2.csv")

def test_check_cluster():
    with pytest.raises(ValueError):
        check_cluster("1.5", "2")

    with pytest.raises(ValueError):
        check_cluster("cat", "dog")
