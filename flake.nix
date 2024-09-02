{
  description = "Harness for the Shopify 2025 internship challenge.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/9a9dae8f6319600fa9aebde37f340975cab4b8c0";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python38
          ];
        };
      });
}
