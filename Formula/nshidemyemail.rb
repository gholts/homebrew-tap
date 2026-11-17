class Nshidemyemail < Formula
  desc "Create iCloud Hide My Email addresses with Apple's native sheet"
  homepage "https://github.com/gholts/NSHideMyEmail"
  url "https://github.com/gholts/NSHideMyEmail/releases/download/v1.0.0/NSHideMyEmail-v1.0.0.tar.gz"
  version "1.0.0"
  sha256 "c001423c476f0a0109cc5e2d53ab374c7173cfd8e7fb786daaaaaf027b2a4dfa"
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
