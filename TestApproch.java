package edd.ovgu.core.constraint.test

import java.nio.file.Path;
import java.nio.file.Paths;

import org.sat4j.specs.TimeoutException;

import de.ovgu.featureide.fm.core.FeatureModelAnalyzer;
import de.ovgu.featureide.fm.core.analysis.cnf.formula.FeatureModelFormula;
import de.ovgu.featureide.fm.core.base.IFeatureModel;
import de.ovgu.featureide.fm.core.init.FMCoreLibrary;
import de.ovgu.featureide.fm.core.init.LibraryManager;
import de.ovgu.featureide.fm.core.io.manager.FeatureModelManager;


public class TestApproch {

    public static void main(String[] args) throws TimeoutException {

        LibraryManager.registerLibrary(FMCoreLibrary.getInstance());
        final Path path = Paths.get("output.xml");
        final IFeatureModel featureM = FeatureModelManager.load(path);

        //Tester si le feature model est vide ou pas.
        if (featureM != null) {
            FeatureModelFormula formula = new FeatureModelFormula(featureM);
            //Analyse du Feature Model
            final FeatureModelAnalyzer analyzer = formula.getAnalyzer();
            analyzer.analyzeFeatureModel(null);
            System.out.println("Feature model is " + (analyzer.isValid(null) ? "not " : "") + "void");
            System.out.println("Dead features: " + analyzer.getDeadFeatures(null));
            extracted(featureM, analyzer);
        }
    }

    private static void extracted(final IFeatureModel featureModel, final FeatureModelAnalyzer analyzer) {
        //Obtenir l'interpretation pour root
        System.out.println(analyzer.getExplanation(featureModel.getFeature("Root")));

        //Obtenir l'interpretation pour Goal racine
        System.out.println(analyzer.getExplanation(featureModel.getFeature("GoalA")));

        //Obtenir l'interpretation pour Feature Racine
        System.out.println(analyzer.getExplanation(featureModel.getFeature("FeatureA")));
    }
}
