from gridlens.cli import main


def test_generate_and_analyze_clean(tmp_path, capsys):
    csv_path = tmp_path / "clean.csv"
    assert main(["generate", str(csv_path), "--duration", "1", "--fs", "10000"]) == 0
    assert main([
        "analyze", str(csv_path), "--interval", "1",
        "--report", str(tmp_path / "report.html"),
        "--json", str(tmp_path / "result.json"),
    ]) == 0
    output = capsys.readouterr().out
    assert "EN 50160" in output
    assert (tmp_path / "report.html").exists()
    assert (tmp_path / "result.json").exists()


def test_generate_distorted_and_bad_file(tmp_path):
    csv_path = tmp_path / "distorted.csv"
    assert main([
        "generate", str(csv_path), "--duration", "1", "--fs", "10000",
        "--harmonic", "5=0.12",
    ]) == 0
    assert main(["analyze", str(csv_path), "--interval", "1"]) == 1
    assert main(["analyze", str(tmp_path / "missing.csv")]) == 2
