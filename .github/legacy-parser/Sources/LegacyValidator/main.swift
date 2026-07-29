import Foundation
import OpenMusicEventParser

@main
enum LegacyValidator {
    static func main() throws {
        let path = CommandLine.arguments.dropFirst().first ?? "."

        do {
            _ = try OrganizerConfiguration.fileTree.read(from: URL(filePath: path))
            print("Parsed successfully. This data can be used in the legacy OpenFestival app.")
        } catch {
            print("Failed to parse: \(error.localizedDescription)")
            throw error
        }
    }
}
