public class Grader {

	public static void main(String[] args){
		int score = 0;
		int scoreMax = 8;
		try{
			if (Quiz1.getSumOfNumbers("aabccccAAA")== 0) {
				System.out.println("Test 1 Passed");
				score += 1;
			}else{
				System.out.println("Test 1 faild");
			}
		}catch(Exception e){
			System.out.println("Test 1 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers("12 some text 3  7") == 22) {
				System.out.println("Test 2 Passed");
				score += 1;
			}else{
				System.out.println("Test 2 faild");
			}
		}catch(Exception e){
			System.out.println("Test 2 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers("12 some text3  7")  == 19) {
				System.out.println("Test 3 Passed");
				score += 1;
			}else{
				System.out.println("Test 3 faild");
			}
		}catch(Exception e){
			System.out.println("Test 3 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers("3some") == 0) {
				System.out.println("Test 4 Passed");
				score += 1;
			}else{
				System.out.println("Test 4 faild");
			}
		}catch(Exception e){
			System.out.println("Test 4 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers("123") == 123) {
				System.out.println("Test 5 Passed");
				score += 1;
			}else{
				System.out.println("Test 5 faild");
			}
		}catch(Exception e){
			System.out.println("Test 5 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers("1 2 3") == 6) {
				System.out.println("Test 6 Passed");
				score += 1;
			}else{
				System.out.println("Test 6 faild");
			}
		}catch(Exception e){
			System.out.println("Test 6 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers(" 1 23 ")== 24) {
				System.out.println("Test 7 Passed");
				score += 1;
			}else{
				System.out.println("Test 7 faild");
			}
		}catch(Exception e){
			System.out.println("Test 7 faild");
		}
		try{
			if (Quiz1.getSumOfNumbers("")==0) {
				System.out.println("Test 8 Passed");
				score += 1;
			}else{
				System.out.println("Test 8 faild");
			}
		}catch(Exception e){
			System.out.println("Test 8 faild");
		}

		System.out.println("Score: " + score + "/" + scoreMax + " = " + (score*30)/scoreMax);
		if (score != scoreMax) {
			System.exit(1);
		} else {
			System.exit(0);
		}
	}

}