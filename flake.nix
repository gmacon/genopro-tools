{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  packages = [ pkgs.ruff ];
                  languages.python = {
                    enable = true;
                    package = pkgs.python3.withPackages (ps: with ps; [
                      click
                      lxml
                      python-lsp-server
                      python-lsp-black
                    ]);
                  };
                }
              ];
            };
          });
    };
}
