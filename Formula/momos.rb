class Momos < Formula
  desc "Offline IPA decryption with a local enrollment model"
  homepage "https://github.com/gholts/momos"
  license all_of: ["Apache-2.0", "MIT", "BSD-2-Clause"]
  head "https://github.com/gholts/momos.git", branch: "main"

  depends_on arch: :arm64
  depends_on macos: :sequoia

  def install
    system "make", "CC=#{ENV.cc}"
    bin.install "build/momos"
    bash_completion.install "completions/momos.bash" => "momos"
    zsh_completion.install "completions/_momos"
    fish_completion.install "completions/momos.fish"
    pkgshare.install "LICENSE", "THIRD-PARTY-NOTICES.txt"
  end
end
