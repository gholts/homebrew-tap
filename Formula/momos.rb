class Momos < Formula
  desc "Offline IPA decryption with a local enrollment model"
  homepage "https://github.com/gholts/momos"
  url "https://github.com/gholts/momos/releases/download/v2.2.0/momos-v2.2.0-macos-arm64.tar.gz"
  sha256 "8db2730cb922eb299df39f5d09518bf434874c72ca76eb468b9775c6ae7f66e6"
  version "2.2.0"
  license all_of: ["Apache-2.0", "MIT", "BSD-2-Clause"]

  depends_on arch: :arm64
  depends_on macos: :sequoia

  def install
    bin.install "momos"
    bash_completion.install "completions/momos.bash" => "momos"
    zsh_completion.install "completions/_momos"
    fish_completion.install "completions/momos.fish"
    pkgshare.install "LICENSE", "THIRD-PARTY-NOTICES.txt"
  end
end
