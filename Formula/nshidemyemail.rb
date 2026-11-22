class Nshidemyemail < Formula
  desc "Create iCloud Hide My Email addresses with Apple's native sheet"
  homepage "https://github.com/gholts/NSHideMyEmail"
  url "https://github.com/gholts/NSHideMyEmail/releases/download/v1.1.0/NSHideMyEmail-v1.1.0.tar.gz"
  version "1.1.0"
  sha256 "8fd2d771025f3c08a32d2f2bb926a2cf7b0fc564063bfc8808f5c6906c836e05"
  license "GPL-3.0-or-later"

  depends_on :macos

  def install
    system "make", "hme"
    bin.install "hme"
  end

  test do
    assert_match "usage: hme", shell_output("#{bin}/hme -h")
  end
end
