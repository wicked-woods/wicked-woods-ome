// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "LegacyValidator",
    platforms: [
        .macOS(.v15),
    ],
    products: [
        .executable(name: "legacy-validator", targets: ["LegacyValidator"]),
    ],
    dependencies: [
        .package(path: "open-music-event/Core"),
    ],
    targets: [
        .executableTarget(
            name: "LegacyValidator",
            dependencies: [
                .product(name: "OpenMusicEventParser", package: "Core"),
            ]
        ),
    ]
)
