{ pkgs, ... }:

pkgs.mkShell {
  name = "jupyter";
  buildInputs = [
    pkgs.python313
    pkgs.python313Packages.cvxpy
    pkgs.python313Packages.jinja2
    pkgs.python313Packages.jupyter
    pkgs.python313Packages.matplotlib
    pkgs.python313Packages.numpy
    pkgs.python313Packages.pandas
    pkgs.python313Packages.psycopg
    pkgs.python313Packages.pydantic
    pkgs.python313Packages.pydantic-settings
    pkgs.python313Packages.pyodbc
    pkgs.python313Packages.requests
    pkgs.python313Packages.scikit-learn
    pkgs.python313Packages.scipy
    pkgs.python313Packages.seaborn
    pkgs.python313Packages.sqlalchemy
    pkgs.python313Packages.statsmodels
    pkgs.python313Packages.sympy
  ];
  shell = pkgs.zsh;
  shellHook = ''
    jupyter lab
  '';
}

