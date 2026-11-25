{
  description = "Description for the project";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ ];
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];
      perSystem = { config, self', inputs', pkgs, system, ... }:
        let
          inherit system;
          pkgs = inputs.nixpkgs.legacyPackages.${system};
          fhs = pkgs.buildFHSEnv {
            name = "Python FHS";
            targetPkgs = (with pkgs; [
              python313Full
              python313Packages.pip
              poetry
            ]);
            runScript = "bash --init-file /etc/profile";
          };
        in
        {
          devShells = {
            fhs = fhs.env;
            default = pkgs.mkShell {
              name = "PostgreSQL 17.5";
              nativeBuildInputs = (with pkgs; [
                python313Full
                python313Packages.pip
                poetry
              ]);
            };
          };
        };
      flake = { };
    };
}
