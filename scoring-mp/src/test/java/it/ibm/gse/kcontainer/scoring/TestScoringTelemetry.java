package it.ibm.gse.kcontainer.scoring;

import org.junit.Assert;
import org.junit.Test;

import ibm.gse.kcontainer.scoring.infrastructure.ScoringClient;
import ibm.gse.kcontainer.scoring.infrastructure.ScoringResult;
import junit.framework.TestCase;
import ibm.gse.kcontainer.scoring.domain.Telemetry;

public class TestScoringTelemetry extends TestCase {

   String URL = "https://zen-cpd-zen.apps.cp4dperf5.demo.ibmcloud.com";
    
    @Test
    public void testEnvVariables() {
        Assert.assertTrue("jboyer".equals(System.getenv("cp4d_user")));
        Assert.assertNotNull(System.getenv("PREDICTION_BASE_URL"));
    }

    @Test
    public void testGetIAMToken(){
        final ScoringClient sc = new ScoringClient(URL,"jboyer","cp4d123");
        Assert.assertNotNull(sc.getIAMToken());
    }

    @Test
    public void testScoringGoodData(){
        final ScoringClient sc = new ScoringClient(URL,"jboyer","cp4d123");
        sc.setPredictiveURL("/v4/deployments/bea7d396-88c5-41fa-a622-1a92deb2bb9e/predictions");
        final Telemetry t = new Telemetry();
        final ScoringResult r = sc.callAnomalyScoring(t);
        Assert.assertNotNull(r);
    }
}