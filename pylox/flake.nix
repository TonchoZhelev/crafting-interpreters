{
  description = "A simple Python development shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }@attrs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          name = "pylox-dev";
          buildInputs = with pkgs; [ 
            (python3.withPackages (ps: with ps; with python3Packages; [
              ipython
            ]))
            nodePackages.pyright
          ];
        };
      }
    );
}
