import com.google.firebase.appdistribution.gradle.firebaseAppDistribution

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.google.services)
    alias(libs.plugins.firebase.appdistribution)
}

android {
    namespace = "com.starnest.ci_cd"
    compileSdk {
        version = release(36)
    }

    defaultConfig {
        applicationId = "com.starnest.ci_cd"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "ci_cd"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        debug {
            firebaseAppDistribution {
                artifactType = "APK"
                releaseNotes = "CI build ${System.getenv("GITHUB_SHA")?.take(7) ?: "local"}"
                testers = System.getenv("FIREBASE_TESTERS_EMAIL").orEmpty()
            }
        }
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            firebaseAppDistribution {
                artifactType = "APK"
                releaseNotes = "CI build ${System.getenv("GITHUB_SHA")?.take(7) ?: "local"}"
                testers = System.getenv("FIREBASE_TESTERS_EMAIL").orEmpty()
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}