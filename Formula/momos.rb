class Momos < Formula
  desc "Offline IPA decryption with a local enrollment model"
  homepage "https://github.com/gholts/momos"
  url "https://github.com/gholts/momos/releases/download/v2.0.0/momos-v2.0.0-macos-arm64.tar.gz"
  sha256 "baf592321b3acfe084d21ef9615ba0f1891db1465d5606b70a1fb181a25dbc57"
  version "2.0.0"
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
