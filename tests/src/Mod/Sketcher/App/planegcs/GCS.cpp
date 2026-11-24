// SPDX-License-Identifier: LGPL-2.1-or-later

#include <gtest/gtest.h>

#include "Mod/Sketcher/App/planegcs/GCS.h"

class SystemTest: public GCS::System
{
public:
    size_t getNumberOfConstraints(int tagID = -1)
    {
        return _getNumberOfConstraints(tagID);
    }
};

class GCSTest: public ::testing::Test
{
protected:
    void SetUp() override
    {
        _system = std::make_unique<SystemTest>();
    }

    void TearDown() override
    {
        _system.reset();
    }

    SystemTest* System()
    {
        return _system.get();
    }

private:
    std::unique_ptr<SystemTest> _system;
};

TEST_F(GCSTest, clearConstraints)  // NOLINT
{
    // Arrange
    const size_t numConstraints {100};
    for (size_t i = 0; i < numConstraints; ++i) {
        System()->addConstraint(new GCS::Constraint());
    }
    ASSERT_EQ(numConstraints, System()->getNumberOfConstraints());

    // Act
    System()->clear();

    // Assert
    EXPECT_EQ(0, System()->getNumberOfConstraints());
}

#ifdef EIGEN_SPARSEQR_COMPATIBLE
TEST_F(GCSTest, sparseDependenciesMatchDenseAndDoNotAccumulate)
{
    double x = 1., y = 2., z = 3., fixed = 9., w = 9., driven = 7., pitch = 1.;
    GCS::VEC_pD params {&x, &y, &z, &w, &driven};
    GCS::VEC_pD drivenParams {&driven};
    for (auto algorithm : {GCS::EigenDenseQR, GCS::EigenSparseQR}) {
        GCS::System system;
        system.autoChooseAlgorithm = false;
        system.qrAlgorithm = algorithm;
        system.declareUnknowns(params);
        system.declareDrivenParams(drivenParams);
        system.addConstraintDifference(&x, &y, &pitch, 1);
        system.addConstraintDifference(&y, &z, &pitch, 2);
        system.addConstraintEqual(&w, &fixed, 3);
        system.addConstraintEqual(&x, &driven, 4, false);
        system.addConstraintEqual(&y, &fixed, -1);
        for (int repeat = 0; repeat < 3; ++repeat) {
            EXPECT_EQ(system.diagnose(), 1);
            GCS::VEC_pD dependent;
            system.getDependentParams(dependent);
            EXPECT_EQ(dependent.size(), 3);
            EXPECT_EQ((std::set<double*>(dependent.begin(), dependent.end())),
                      (std::set<double*> {&x, &y, &z}));
            EXPECT_FALSE(system.hasConflicting());
            EXPECT_FALSE(system.hasRedundant());
        }
    }
}

TEST_F(GCSTest, sparseDiagnosisRetainsRedundancyAndConflictChecks)
{
    for (bool conflicting : {false, true}) {
        double x = 2., first = 2., second = conflicting ? 3. : 2.;
        GCS::VEC_pD params {&x};
        GCS::System system;
        system.autoChooseAlgorithm = false;
        system.qrAlgorithm = GCS::EigenSparseQR;
        system.declareUnknowns(params);
        system.addConstraintEqual(&x, &first, 1);
        system.addConstraintEqual(&x, &second, 2);
        system.diagnose();
        EXPECT_EQ(system.hasConflicting(), conflicting);
        EXPECT_EQ(system.hasRedundant(), !conflicting);
    }
}

TEST_F(GCSTest, sparseSharedParameterAndZeroRank)
{
    double x = 2., difference = 0.;
    GCS::VEC_pD params {&x, &difference};
    for (auto algorithm : {GCS::EigenDenseQR, GCS::EigenSparseQR}) {
        GCS::System system;
        system.autoChooseAlgorithm = false;
        system.qrAlgorithm = algorithm;
        system.declareUnknowns(params);
        system.addConstraintDifference(&x, &x, &difference, 1);
        EXPECT_EQ(system.diagnose(), 1);
        GCS::VEC_pD dependent;
        system.getDependentParams(dependent);
        EXPECT_EQ(dependent, (GCS::VEC_pD {&x}));
    }
    GCS::System system;
    system.autoChooseAlgorithm = false;
    system.qrAlgorithm = GCS::EigenSparseQR;
    system.declareUnknowns(params);
    system.addConstraintEqual(&x, &x, 1);
    EXPECT_EQ(system.diagnose(), 2);
    GCS::VEC_pD dependent;
    system.getDependentParams(dependent);
    EXPECT_EQ(dependent.size(), 2);
}
#endif
