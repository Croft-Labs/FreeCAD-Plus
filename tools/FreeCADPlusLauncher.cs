// SPDX-License-Identifier: LGPL-2.1-or-later
// Portable owner launcher: retain native exit status and forward exact arguments.
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;

internal static class FreeCADPlusLauncher
{
    private static string Quote(string value)
    {
        var result = new StringBuilder("\"");
        int slashes = 0;
        foreach (char ch in value) {
            if (ch == '\\') { slashes++; continue; }
            if (ch == '"') { result.Append('\\', slashes * 2 + 1); result.Append(ch); }
            else { result.Append('\\', slashes); result.Append(ch); }
            slashes = 0;
        }
        result.Append('\\', slashes * 2); result.Append('"');
        return result.ToString();
    }

    [STAThread]
    private static int Main(string[] args)
    {
        string root = AppDomain.CurrentDomain.BaseDirectory;
        var start = new ProcessStartInfo(Path.Combine(root, "bin", "FreeCAD.exe"));
        start.WorkingDirectory = root;
        start.UseShellExecute = false;
        start.Arguments = string.Join(" ", args.Select(Quote));
        using (var child = Process.Start(start)) {
            if (child == null) return 1;
            child.WaitForExit();
            return child.ExitCode;
        }
    }
}
